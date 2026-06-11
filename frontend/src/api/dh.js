import api from './index'

export function dhExchange(p, g, aPrivate, bPrivate) {
  return api.post('/dh/exchange', { p, g, a_private: aPrivate, b_private: bPrivate })
}

export function dhMitm(p, g, aPrivate, bPrivate, mPrivate) {
  return api.post('/dh/mitm', { p, g, a_private: aPrivate, b_private: bPrivate, m_private: mPrivate })
}

export function colorMixing(aliceColor, bobColor, commonColor) {
  return api.post('/dh/color-mixing', {
    alice_private_color: aliceColor,
    bob_private_color: bobColor,
    common_color: commonColor,
  })
}
