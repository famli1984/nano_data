# Infrastructure

*Hosting, domain, accounts, and stack for Entropic.*

*Last updated: 2026-05-10*

---

## Domain

> ❓ Question: What domain do we want? Options to check:
> - entropic.io (international, tech feel)
> - entropic.de (German-first)
> - entropic-founders.com (descriptive)
> - joinentropic.com (action-oriented)

Check availability before deciding. Register with Cloudflare Registrar (no markup, DSGVO-friendly DNS).

---

## Tech Stack

We build AI-native from day one. The Entropic platform is also a showcase of what we teach.

| Layer | Tool | Notes |
|-------|------|-------|
| **Landing page** | Carrd or Framer | Fast, no-code, looks good |
| **Community** | Circle.so | Purpose-built for communities, better than Slack for async |
| **Curriculum / LMS** | Notion or self-built | Start simple — Notion works for the first 50 members |
| **Agent framework** | Claude API + custom | We build this — it's our core IP |
| **Shell company ops** | Manual → automated | First 10 are manual; then we build the workflow |
| **Payments** | Stripe | Standard, fast to set up |
| **Email** | Beehiiv or MailerLite | For newsletter + curriculum delivery |
| **Auth** | Clerk + Supabase | If we build a real web app |
| **Hosting** | Vercel / Railway | Standard, EU region for DSGVO |
| **AI backbone** | Anthropic Claude | Primary; OpenAI as fallback |

---

## DSGVO Requirements

- All servers in EU (Frankfurt/Ireland preferred)
- No US-based analytics without explicit consent (no Google Analytics by default)
- Privacy policy and cookie consent before any data collection
- Shell companies we set up for customers: no customer data stored in AI — all anonymous/templated

---

## Account Checklist (Day 1)

- [ ] Domain registered
- [ ] Cloudflare account set up (DNS + basic security)
- [ ] Anthropic API access (for agent framework)
- [ ] Stripe account (for payments)
- [ ] Circle.so account (community)
- [ ] GitHub organization for shared code
- [ ] Notion workspace (curriculum + internal docs)
- [ ] Business email (hello@entropic.io or similar)
- [ ] 1Password shared vault (both founders)
