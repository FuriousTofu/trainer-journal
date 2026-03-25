# TrainerJournal

#### Description:

TrainerJournal is a comprehensive web application designed for personal fitness trainers to manage their clients, training sessions, exercises, and business operations. Built as my CS50 final project, it has evolved into a production-ready tool currently used by three alpha testers in real training environments.

## 🔔 Updates

#### 25/03/2026 v 0.1.1:
- **Tag system**: create, edit, and delete custom color-coded tags to label sessions (up to 4 per session)
- **Home dashboard**: today's sessions and unpaid sessions overview on the main page
- **Quick actions**: toggle session status (planned/done) and payment status directly from session tables via HTMX
- **Overdue sessions**: planned sessions past their end time are now visually highlighted
- **Removed session mode**: online/in-person distinction dropped from the entire project
- **Payment badges**: redesigned as interactive inline icons
- **UI cleanup**: refactored client/session tables with reusable macros and helpers

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
The session management system allows trainers to schedule training sessions with specific start times, duration, and pricing. Each session can include multiple exercises with sets, reps, and weight tracking. The system displays exercise history from previous sessions, helping trainers make informed programming decisions. Sessions can be marked as planned, done, cancelled or no-show, with payment tracking for business operations. Trainers can create custom color-coded tags and assign up to four tags per session, making it easy to categorize and visually distinguish different types of training.

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
- Session filters and sorting
- 1RM calculations for periodization planning
- Client progress graphs and search functionality


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