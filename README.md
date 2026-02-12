# TrainerJournal

#### Video Demo: https://youtu.be/Uc07ZfU6lkk?si=4_O87wxzFZAD7Lgy

#### Description:

TrainerJournal is a comprehensive web application designed for personal fitness trainers to manage their clients, training sessions, exercises, and business operations. Built as my CS50 final project, it has evolved into a production-ready tool currently used by three alpha testers in real training environments.

## 🛠️ Technology Stack

The application is built using:
- **Backend**: Python Flask with SQLAlchemy ORM
- **Database**: PostgreSQL with Alembic for migrations
- **Frontend**: Bootstrap 5 for responsive UI, HTMX for dynamic interactions, TomSelect for form controls
- **Authentication**: Flask-Login with bcrypt password hashing
- **Security**: Flask-Limiter for rate limiting, Flask-WTF for CSRF protection
- **Deployment**: Railway platform with Cloudflare for security and performance

## ✨ Core Features

### Client Management
Trainers can create and manage client profiles with contact information, session pricing, and custom notes. Clients can be marked as active or on pause — paused clients remain visible in the main list but cannot have new sessions scheduled. Clients can be archived (read-only access in a separate tab) or permanently deleted (and removing all associated sessions).

### Session Scheduling
The session management system allows trainers to schedule training sessions with specific start times, duration, mode (online/in-person), and pricing. Each session can include multiple exercises with sets, reps, and weight tracking. The system displays exercise history from previous sessions, helping trainers make informed programming decisions. Sessions can be marked as planned, done, cancelled or no-show, with payment tracking for business operations.

### Exercise Library
Trainers maintain a personal exercise database with names and descriptions. Exercises can be archived when no longer used but are never deleted if referenced in session history. The system supports creating new exercises on-the-fly during session planning through TomSelect's create functionality, streamlining the workflow.

### Payment Tracking
Each session tracks payment status and automatically records payment dates when marked as paid. This provides trainers with clear financial oversight of their business operations.

## 📁 Project Structure

### Application Configuration (`app/config.py`, `app/__init__.py`)
The configuration system separates development and production settings, loading sensitive credentials from environment variables. The application factory pattern in `__init__.py` initializes Flask extensions including SQLAlchemy, Flask-Login, CSRF protection, and rate limiting.

### Database Models (`app/models.py`)
The database schema defines five main tables: Trainers (user accounts), Clients, Exercises, Sessions, and SessionExercises (junction table). I chose to use nanoid for generating public IDs instead of exposing database integer IDs in URLs for security. The schema includes comprehensive constraints: CHECK constraints ensure data validity (non-negative prices, positive durations), UNIQUE constraints prevent duplicate client/exercise names per trainer, and proper CASCADE/RESTRICT rules maintain referential integrity—when a client is deleted, all their sessions are removed; when a trainer is deleted, all their clients and exercises are removed.

### Forms (`app/forms/`)
WTForms handles all form validation with custom validators. I separated forms into domain-specific files (clients.py, exercises.py, sessions.py, user.py) for maintainability. The session form uses FieldList for dynamic exercise rows, allowing unlimited exercises per session while maintaining validation. This was a key design decision over a fixed number of exercise inputs.

### Routes (`app/routes/`)
Routes are organized by domain with a Blueprint pattern. The sessions.py file is the most complex, handling HTMX requests for dynamic exercise rows, exercise history display, and client price auto-population.

### Security Implementation
Multi-layered security includes Cloudflare rules blocking suspicious traffic, Flask-Limiter preventing brute force attacks (20 requests/minute default), CSRF tokens on all POST forms, and bcrypt password hashing with 256-character hash storage. Public IDs use nanoid with retry logic to ensure uniqueness without exposing database structure.

### Frontend JavaScript (`app/static/js/`)
The JavaScript is purposefully minimal. `session-form.js` handles TomSelect initialization for exercise dropdowns, including reinitializing after HTMX adds new rows. `ex-history.js` triggers history refreshes when the client changes. `table-row-link.js` makes table rows clickable for navigation. I chose this approach over heavy client-side frameworks because the application's interaction patterns don't require complex state management.

### Templates (`app/templates/`)
Jinja2 templates use inheritance for consistent layouts. The `layout.html` defines the sidebar navigation and mobile bottom nav, detecting the current route to highlight active pages. Sessions and clients have separate templates for active vs archived states. I used Bootstrap's utility classes extensively to avoid writing custom CSS.

### Database Utilities (`app/utils/`)
The `database.py` file contains nanoid generation logic with retry mechanisms. The `template_filters.py` defines custom Jinja filters like `dt_no_seconds` for datetime formatting in the Europe/Kyiv timezone. This centralization prevents code duplication across templates.

## 🚀 Current State and Future Plans

The application successfully handles three active trainers managing real clients and sessions. Current development focuses on mobile responsiveness improvements based on user feedback.

**Planned Features:**
- AI assistant for client progress analysis
- Error handlers and feedback mechanisms
- Comprehensive testing suite
- User settings: timezone, currency, units of measurement
- Password recovery and Google login
- Dashboard with upcoming sessions and payment summaries
- Time-based exercise completion tracking
- Session filters and sorting
- 1RM calculations for periodization planning
- Client progress graphs and search functionality

This project taught me practical web development beyond tutorial projects: handling real user feedback, implementing security layers, managing database migrations in production, and making pragmatic technology choices based on actual needs rather than hype.

## 🤝 Development Journey and AI Assistance

This project was developed with assistance from Claude (Anthropic's AI), which played a significant role in accelerating learning and solving complex problems.

### Complex Implementation Challenges

**Dynamic Form Handling with HTMX**
The exercise rows feature required understanding how WTForms FieldList works with HTMX. Claude explained how to properly name form fields for server-side validation and manage TomSelect reinitialization after HTMX swaps DOM elements.

**Database Migrations**
When adding time-based exercise support, Claude helped design the migration strategy with nullable `reps`, XOR constraints, and defensive migration code that checks for existing constraints before dropping them.

### 💻 JavaScript Implementation
Unlike the Python backend where I consulted Claude but worked through understanding each piece myself, **I largely delegated JavaScript implementation to Claude**. The `session-form.js`, `ex-history.js`, and `table-row-link.js` files were mostly AI-generated. However, I made sure to review and understand post-factum how TomSelect initialization works, why HTMX event listeners (`htmx:afterSwap`, `htmx:afterSettle`) are needed, and how the event delegation pattern functions. This taught me practical JavaScript patterns even though I didn't write the code myself initially.

### Code Review and Best Practices
Claude reviewed code for SQL injection prevention, N+1 query problems (using `selectinload`), resource cleanup, and input validation edge cases.

### Learning Approach
I used Claude as a **senior developer mentor** rather than a code generator:
1. Attempt implementation myself first
2. Ask Claude to review and explain issues
3. Understand the *why* before applying fixes
4. Ask follow-up questions until concepts are clear
5. Apply learned patterns to new features independently

This approach meant slower initial development but deeper understanding. By the end, I was implementing new features with minimal assistance because I understood the underlying patterns.

### 💡 Key Insight
**AI accelerates learning but doesn't replace understanding.** 
The most significant challenge I faced was implementing the backend for the dynamic exercise form. After days of brainstorming and documentation review, I developed a solution independently. This experience significantly boosted my confidence and shaped my current perspective on how I see my role in the development workflow.

## 🎯 Challenges and Learning Points

### Post-CS50 Onboarding
Leaving the comfortable CS50 ecosystem was initially overwhelming. The abundance of choices—which technologies to use, which deployment platforms to choose—created analysis paralysis. The real world doesn't come with predefined toolchains. The pressure was intense in the early days. Every decision felt high-stakes: Flask vs Django vs FastAPI? SQLAlchemy vs raw SQL? HTMX vs React? These weren't just technical choices—they affected the entire project trajectory.

### SQLAlchemy + Alembic Learning Curve
Moving from CS50's simple SQLite to production PostgreSQL with ORM and migrations was challenging. Understanding how SQLAlchemy's session management works, why `db.session.flush()` is needed before accessing auto-generated IDs, and how Alembic tracks schema changes required significant mental overhead.

### AI Balance
CS50's guidance to "treat such tools as amplifying, not supplanting, your productivity" proved crucial. Finding the right balance between using AI for acceleration and ensuring genuine understanding required discipline.

### Scope Creep
I constantly struggled with feature scope: timezones, multi-currency support, client-side logins, multi-trainer support, payment entities, future-proofing database indexes. Learning to ship MVP features and iterate based on feedback was a valuable lesson.

### When Is It Done?
There was always "one more feature" before showing it to users. But feedback from actual trainers was invaluable—I should have deployed earlier. Real user input beats perfectionism.

## 📄 License

This project is available for **non-commercial use only** under a custom license.

### You CAN:
- ✅ Use it for your gym, personal training, or any free service
- ✅ Modify and improve the code
- ✅ Learn from it and share it
- ✅ Run it for yourself or others at no charge

### You CANNOT:
- ❌ Sell it as a product
- ❌ Offer it as a paid SaaS service
- ❌ Use it commercially without permission

### Attribution Required:
Please link back to this repository in any public-facing use.

**Interested in commercial use?** Contact me via [GitHub](https://github.com/FuriousTofu) for licensing options.

See the [LICENSE](LICENSE) file for full details.