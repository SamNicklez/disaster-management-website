import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { user } from '../../stores/user.js'

beforeEach(() => {
  setActivePinia(createPinia())
})

describe('User Store', () => {
  it('initializes with default state', () => {
    const userStore = user()
    expect(userStore.username).toBe('')
    expect(userStore.token).toBe('')
    expect(userStore.refreshDate).toBeNull()
    expect(userStore.loginAttempts).toBe(0)
    expect(userStore.lastLoginAttempt).toBeNull()
  })

  it('setLogin sets user data correctly', () => {
    const userStore = user()
    userStore.setLogin('testUser', 'testToken')
    expect(userStore.username).toBe('testUser')
    expect(userStore.token).toBe('testToken')
    expect(userStore.refreshDate).not.toBeNull()
    expect(userStore.lastLoginAttempt).not.toBeNull()
  })

  it('setLogout clears user data correctly', () => {
    const userStore = user()
    userStore.setLogout()
    expect(userStore.username).toBe('')
    expect(userStore.token).toBe('')
    expect(userStore.refreshDate).toBeNull()
  })

  it('setLoginAttempt increments login attempts', () => {
    const userStore = user()
    userStore.setLoginAttempt()
    expect(userStore.loginAttempts).toBe(1)
  })

  it('resetLoginAttempts resets login attempts to 0', () => {
    const userStore = user()
    // Simulate a few login attempts
    userStore.setLoginAttempt()
    userStore.setLoginAttempt()
    // Reset attempts
    userStore.resetLoginAttempts()
    expect(userStore.loginAttempts).toBe(0)
  })

  it('expired getter calculates expiration correctly', () => {
    const userStore = user()
    userStore.setDate()
    expect(userStore.expired).toBe(true)
  })
})

describe('User Store Getters', () => {
  let userStore

  beforeEach(() => {
    // Reset the store before each test
    const pinia = createPinia()
    setActivePinia(pinia)
    userStore = user()
  })

  it('getLoginAttempts returns the correct number of login attempts', () => {
    // Initially, there should be no login attempts
    expect(userStore.getLoginAttempts).toBe(0)

    // Simulate a login attempt
    userStore.setLoginAttempt()
    expect(userStore.getLoginAttempts).toBe(1)

    userStore.setLoginAttempt()
    expect(userStore.getLoginAttempts).toBe(2)
  })

  it('getLastLoginAttemptTime returns the correct time of the last login attempt', () => {
    expect(userStore.getLastLoginAttemptTime).toBeNull()

    // Simulate a login attempt
    userStore.setLoginAttempt()
    const firstAttemptTime = userStore.lastLoginAttempt
    expect(userStore.getLastLoginAttemptTime).toBe(firstAttemptTime)

    return new Promise((resolve) => {
      setTimeout(() => {
        userStore.setLoginAttempt()
        const secondAttemptTime = userStore.lastLoginAttempt
        expect(userStore.getLastLoginAttemptTime).toBe(secondAttemptTime)
        expect(secondAttemptTime).not.toBe(firstAttemptTime)
        resolve()
      }, 1000)
    })
  })
})
