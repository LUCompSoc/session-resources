addEventListener("scheduled", event => event.waitUntil(sendMessage("cron woof")))

addEventListener("fetch", event => {
  event.waitUntil(sendMessage("fetch woof"))
  event.respondWith(
    new Response(
      JSON.stringify({ ok: true })
    )
  )
})


function sendMessage(message) {
  fetch(
    'https://discord.com/api/webhooks/1204013547458400266/mWtRzXZEZP2EWHrXLhQy1eFre8KeOV-vcsKGx5fAYrVzRA46AsXoPBUGzwTUOOlCbnjG',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: message })
    }
  )
}

