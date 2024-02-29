import { describe, it, expect, beforeEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { user } from '@/stores/user'

describe('user store', () => {
  beforeEach(() => {
    // Reset Pinia state before each test
    setActivePinia(createPinia())
  })

  it('sets user login data correctly', () => {
    const userStore = user()
    const username = 'testUser'
    const token = 'testToken'
    userStore.setLogin(username, token)

    expect(userStore.username).toBe(username)
    expect(userStore.token).toBe(token)
    expect(userStore.refreshDate).toBeInstanceOf(Date)
    expect(userStore.lastLoginAttempt).toBeInstanceOf(Date)
  })

  it('resets user data on logout', () => {
    const userStore = user()
    userStore.setLogout()

    expect(userStore.username).toBe('')
    expect(userStore.token).toBe('')
    expect(userStore.refreshDate).toBeNull()
  })

  it('increments login attempts', () => {
    const userStore = user()
    userStore.setLoginAttempt()
    userStore.setLoginAttempt()

    expect(userStore.loginAttempts).toBe(2)
  })

  it('resets login attempts', () => {
    const userStore = user()
    userStore.setLoginAttempt()
    userStore.resetLoginAttempts()

    expect(userStore.loginAttempts).toBe(0)
  })

  it('clears user data', () => {
    const userStore = user()
    userStore.setLogin('testUser', 'testToken')
    userStore.clearUser()

    expect(userStore.username).toBe('')
    expect(userStore.token).toBe('')
    expect(userStore.refreshDate).toBeNull()
    expect(userStore.loginAttempts).toBe(0)
    expect(userStore.lastLoginAttempt).toBeNull()
  })

  it('checks if token is expired correctly', () => {
    const userStore = user()
    // Set refreshDate to a past date
    const pastDate = new Date()
    pastDate.setMinutes(pastDate.getMinutes() - 20)
    userStore.refreshDate = pastDate

    expect(userStore.expired).toBe(false)
  })

  it('gets token as string', () => {
    const userStore = user()
    userStore.setLogin('testUser', 'testToken')

    expect(userStore.getToken).toBe('testToken')
  })
})
