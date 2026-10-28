import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User, Organization } from '../types'

interface AuthState {
  token: string | null;
  user: User | null;
  currentOrg: Organization | null;
  organizations: Organization[];
  setAuth: (token: string, user: User) => void;
  setCurrentOrg: (org: Organization) => void;
  setOrganizations: (orgs: Organization[]) => void;
  logout: () => void;
  isAuthenticated: () => boolean;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      token: null,
      user: null,
      currentOrg: null,
      organizations: [],
      setAuth: (token, user) => set({ token, user }),
      setCurrentOrg: (org) => set({ currentOrg: org }),
      setOrganizations: (orgs) => set({ organizations: orgs }),
      logout: () => set({ token: null, user: null, currentOrg: null, organizations: [] }),
      isAuthenticated: () => !!get().token && !!get().user,
    }),
    { name: 'ecotrack-auth' }
  )
)
