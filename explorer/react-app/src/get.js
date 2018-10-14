import settings from './settings'

export default async action => {
  const req = await fetch(settings.API_URL + '/' + action, {
    credentials: 'include'
  })
  if (req.status !== 200) {
    throw new Error()
  }
  const res = await req.json()
  return res
}
