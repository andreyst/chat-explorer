import settings from './settings'

export default async (action, body) => {
  const req = await fetch(settings.API_URL + '/' + action, {
    credentials: 'include',
    method: 'POST',
    body: body
  })
  if (req.status !== 200) {
    throw new Error()
  }
  const res = await req.json()
  return res
}
