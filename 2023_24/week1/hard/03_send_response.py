import struct
from pprint import pprint

import lib
from lib import *


def parse_dns_request(query_data: bytes) -> DNSMessage:
    if len(query_data) < 12:
        raise ValueError('Invalid DNS request data')

    header, offset = parse_dns_header(query_data)
    questions = parse_dns_questions(query_data, offset, header.question_count)

    dns_message = DNSMessage(header=header, questions=questions)
    return dns_message


def parse_dns_header(query_data: bytes) -> tuple[DNSHeader, int]:
    (
        transaction_id,
        flags,
        question_count,
        answer_count,
        authority_count,
        additional_count,
    ) = struct.unpack('!HHHHHH', query_data[:12])

    is_response = (flags & 0x8000) >> 15
    opcode = (flags & 0x7800) >> 11
    is_authoritative_answer = (flags & 0x0400) >> 10
    is_truncated = (flags & 0x0200) >> 9
    is_recursion_desired = (flags & 0x0100) >> 8
    is_recursion_available = (flags & 0x0080) >> 7
    response_code = (flags & 0x000F)

    dns_flags = DNSFlags(
        is_response=bool(is_response),
        opcode=DNSOpcode(opcode),
        is_authoritative_answer=bool(is_authoritative_answer),
        is_truncated=bool(is_truncated),
        is_recursion_desired=bool(is_recursion_desired),
        is_recursion_available=bool(is_recursion_available),
        response_code=response_code
    )

    header = DNSHeader(
        transaction_id=transaction_id,
        flags=dns_flags,
        question_count=question_count,
        answer_count=answer_count,
        authority_count=authority_count,
        additional_count=additional_count
    )

    return header, 12  # Return header and offset after the header


def parse_dns_questions(query_data: bytes, offset: int, question_count: int) -> list[DNSQuestion]:
    questions = []
    for _ in range(question_count):
        question_name, offset = parse_dns_name(query_data, offset)
        qtype, qclass = struct.unpack('!HH', query_data[offset:offset + 4])
        question = DNSQuestion(question_name, DNSRecordType(qtype), DNSClass(qclass))
        offset += 4
        questions.append(question)
    return questions



def parse_dns_name(data: bytes, offset: int) -> tuple[str, int]:
    labels = []
    while True:
        length = data[offset]
        if length == 0:
            break
        if length & 0xC0 == 0xC0:
            pointer = struct.unpack('!H', data[offset:offset + 2])[0] & 0x3FFF
            return '.'.join(labels), pointer
        offset += 1
        label = data[offset:offset + length].decode('utf-8')
        labels.append(label)
        offset += length
    return '.'.join(labels), offset + 1


def serialize_response(dns_message: DNSMessage) -> bytes:
    # Serialize the DNS header
    header_bytes = struct.pack(
        '!HHHHHH',
        dns_message.header.transaction_id,
        _serialize_flags(dns_message.header.flags),
        dns_message.header.question_count,
        dns_message.header.answer_count,
        dns_message.header.authority_count,
        dns_message.header.additional_count,
    )

    # Serialize the DNS questions
    question_bytes = b''.join(
        _serialize_question(question) for question in dns_message.questions
    )

    # Serialize the DNS answers, authorities, and additional sections
    answer_bytes = b''.join(
        _serialize_resource_record(record) for record in dns_message.answers
    )
    authority_bytes = b''.join(
        _serialize_resource_record(record) for record in dns_message.authorities
    )
    additional_bytes = b''.join(
        _serialize_resource_record(record) for record in dns_message.additional
    )

    # Combine all the serialized parts to form the complete DNS response
    response_bytes = header_bytes + question_bytes + answer_bytes + authority_bytes + additional_bytes

    return response_bytes


def _serialize_flags(flags: DNSFlags) -> int:
    # Calculate the flags field by combining individual flag bits
    qr = (1 if flags.is_response else 0) << 15
    opcode = (flags.opcode.value & 0x0F) << 11
    aa = (1 if flags.is_authoritative_answer else 0) << 10
    tc = (1 if flags.is_truncated else 0) << 9
    rd = (1 if flags.is_recursion_desired else 0) << 8
    ra = (1 if flags.is_recursion_available else 0) << 7
    response_code = flags.response_code & 0x0F

    # Combine the flag bits to form the flags field
    flags_field = qr | opcode | aa | tc | rd | ra | response_code

    return flags_field


def _serialize_question(question: DNSQuestion) -> bytes:
    # Serialize a DNS question
    qname = _serialize_name(question.name)
    qtype = struct.pack('!H', question.typ.value)
    qclass = struct.pack('!H', question.cls.value)

    return qname + qtype + qclass


def _serialize_name(name: str) -> bytes:
    # Serialize a DNS domain name
    labels = name.split('.')
    name_bytes = b''
    for label in labels:
        length = len(label)
        name_bytes += struct.pack('B', length) + label.encode('utf-8')
    name_bytes += b'\x00'  # Terminate with a null byte

    return name_bytes


def _serialize_resource_record(record: DNSResourceRecord) -> bytes:
    # Serialize a DNS resource record
    rr_name = _serialize_name(record.name)
    rr_type = struct.pack('!H', record.typ.value)
    rr_class = struct.pack('!H', record.cls.value)
    rr_ttl = struct.pack('!I', record.ttl)
    rr_data_length = struct.pack('!H', record.data_length)
    rr_data = record.data

    return rr_name + rr_type + rr_class + rr_ttl + rr_data_length + rr_data


# Create a DNS response function
def create_dns_response(query_data: bytes):
    request = parse_dns_request(query_data)
    pprint(request)

    location = socket.inet_aton('192.168.0.100')
    response = DNSMessage(
        header=DNSHeader(
            transaction_id=request.header.transaction_id,
            flags=DNSFlags(
                is_response=True,
                opcode=DNSOpcode.QUERY,
                is_authoritative_answer=False,
                is_truncated=False,
                is_recursion_desired=True,
                is_recursion_available=False,
                response_code=0,
            ),
            question_count=0,
            answer_count=1,
            authority_count=0,
            additional_count=0,
        ),
        answers=[
            DNSResourceRecord(
                name='example.com',
                typ=DNSRecordType.A,
                cls=DNSClass.IN,
                ttl=3600,
                data_length=len(location),
                data=location,
            )
        ]
    )
    pprint(response)
    
    return serialize_response(response)


if __name__ == '__main__':
    exit(lib.dns_server(create_dns_response))
