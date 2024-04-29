const fastify = require('fastify')
const os = require('os')

const app = fastify({
  logger: {
    enabled: 'true',
    level: 'debug',
    serializers: {
      req (request) {
        return {
          method: request.method,
          url: request.url,
          headers: request.headers,
          hostname: request.hostname,
          remoteAddress: request.ip,
          remotePort: request.socket.remotePort
        }
      }
    }
  },
})

app.get('/ok', (_request, reply) =>{
  reply.code(200).send(`Hi from ${os.hostname}`)
})

app.listen(
  {
    port: process.env.PORT ?? 3000,
    host: '0.0.0.0'
  }, (error, _address) => {
    if (error) {
      console.error(error)
      return
    }
  }
)
