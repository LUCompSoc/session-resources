
async function sendMessage(message) {
  const dog = await fetch('https://random.dog/woof.json').then(res => res.json()).then(dog => dog.url)
  fetch(
    'https://discord.com/api/webhooks/1204013547458400266/mWtRzXZEZP2EWHrXLhQy1eFre8KeOV-vcsKGx5fAYrVzRA46AsXoPBUGzwTUOOlCbnjG',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        embeds: [
          {
            title: 'A friend',
            description: 'Let me introduce you to one of my friends.',
            image: {
              url: dog,
            },
            author: {
              name: "Rover",
              url: 'https://en.wikipedia.org/wiki/Office_Assistant',
              icon_url: 'https://mklab.eu.org/clippy/images/clippy/rover.png',
            },
            color: 0xffb91d,
          }
        ]
      })
    }
  )
    .then(res => res.text())
    .then(console.log)
    .catch(console.error)
}

sendMessage()

