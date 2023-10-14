from __future__ import annotations

import socket
import warnings
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum


# DNS Record Type
class DNSRecordType(Enum):
    UNKNOWN = 0
    A = 1           # IPv4 address
    AAAA = 28       # IPv6 address
    CNAME = 5       # Canonical name
    MX = 15         # Mail exchange
    NS = 2          # Name server
    PTR = 12        # Pointer
    SOA = 6         # Start of authority
    SRV = 33        # Service locator
    TXT = 16        # Text
    OPT = 41

    @classmethod
    def from_int(cls, value: int) -> DNSRecordType:
        try:
            return cls(value)
        except ValueError:
            warnings.warn(f'Unknown DNS record type {value}')
            return cls.UNKNOWN


# DNS Class
class DNSClass(Enum):
    UNKNOWN = 0
    IN = 1
    CH = 3  # Chaosnet
    HS = 4  # Hesiod
    NONE = 254  # NONE (used in dynamic updates)
    ANY = 255  # Wildcard match for all classes

    @classmethod
    def from_int(cls, value: int) -> DNSClass:
        try:
            return cls(value)
        except ValueError:
            warnings.warn(f'Unknown DNS class {value}')
            return cls.UNKNOWN


# Enum for DNS OPCODE (Operation Code)
class DNSOpcode(Enum):
    QUERY = 0
    IQUERY = 1
    STATUS = 2
    NOTIFY = 4
    UPDATE = 5


@dataclass
class DNSFlags:
    is_response: bool  # 'Query' (0) / 'Response' (1)
    opcode: DNSOpcode  # Operation Code (4 bits)
    is_authoritative_answer: bool  # 'Authoritative Answer'
    is_truncated: bool  # 'Truncation'
    is_recursion_desired: bool  # 'Recursion Desired'
    is_recursion_available: bool  # 'Recursion Available'
    response_code: int  # 'Response Code' (4 bits)


# DNS Header
@dataclass
class DNSHeader:
    transaction_id: int
    flags: DNSFlags
    question_count: int
    answer_count: int
    authority_count: int
    additional_count: int


# DNS Question
@dataclass
class DNSQuestion:
    name: str
    typ: DNSRecordType
    cls: DNSClass


# DNS Resource Record (RR)
@dataclass
class DNSResourceRecord:
    name: str
    typ: DNSRecordType
    cls: DNSClass
    ttl: int
    data_length: int
    data: bytes


# DNS Message
@dataclass
class DNSMessage:
    header: DNSHeader
    questions: list = field(default_factory=list)
    answers: list = field(default_factory=list)
    authorities: list = field(default_factory=list)
    additional: list = field(default_factory=list)


# DNS Server
def dns_server(handler_func: Callable[[bytes], bytes]):
    DNS_SERVER_IP = '0.0.0.0'
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((DNS_SERVER_IP, 0))
        _, server_port = server_socket.getsockname()
        print(f'DNS server listening on {DNS_SERVER_IP}:{server_port}')

        while True:
            try:
                query_data, client_address = server_socket.recvfrom(1024)
                response_data = handler_func(query_data)
                server_socket.sendto(response_data, client_address)
                print(f'Response sent to {client_address}')
            except KeyboardInterrupt:
                break


class UpstreamServer:
    def __init__(self, host: str, port: int = 53) -> None:
        self.host = host
        self.port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __enter__(self) -> UpstreamServer:
        self._socket.connect((self.host, self.port))
        return self

    def __exit__(self, *_) -> bool:
        self._socket.close()
        return False

    def query(self, data: bytes) -> bytes:
        self._socket.sendall(data)
        return self._socket.recv(1024)

