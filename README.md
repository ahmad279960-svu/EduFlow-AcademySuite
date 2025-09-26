# EduFlow-AcademySuite v2.0

**EduFlow-AcademySuite v2.0** is a data-driven, monolithic-modular Learning Experience Platform (LXP) designed for educational institutions and corporate training centers that require high-fidelity performance tracking, deep analytics, and absolute data integrity. This version represents a strategic re-architecture from its predecessor, migrating from MongoDB to a robust PostgreSQL backend to enable advanced relational data modeling and complex querying capabilities.

The platform combines a modern, reactive user interface powered by **HTMX** with a powerful **Django** backend, delivering a seamless and responsive user experience without the complexity of traditional single-page applications.

## Core Philosophy

The core philosophy of v2.0 is to **empower impactful education through an integrated and reliable architecture**. We transition from a model of "ultimate flexibility" to one of "intelligent reliability," where data integrity and analytical depth are paramount.

## Key Features

* **Modular Architecture**: Built as a "Majestic Monolith," the system is a single deployable unit with a codebase that is strictly organized into decoupled Django apps, ensuring low coupling and high cohesion.
* **Data-Driven Analytics**: Leverages the power of PostgreSQL for complex queries, enabling the generation of detailed, multi-dimensional reports for administrators, supervisors, and B2B clients.
* **Reactive Frontend**: Utilizes HTMX to create a fast, SPA-like user experience with server-side rendering, simplifying the frontend stack and accelerating development.
* **Role-Based Access Control (RBAC)**: A comprehensive permissions system based on user roles (Admin, Supervisor, Instructor, Student, B2B Client) to ensure users can only access relevant features and data.
* **Scalable Infrastructure**: Designed to be stateless and horizontally scalable, utilizing Celery for asynchronous task processing and Docker for containerization, ensuring consistent environments from development to production.

## Technology Stack

| Component                | Technology                                         | Rationale                                                                        |
| ------------------------ | -------------------------------------------------- | -------------------------------------------------------------------------------- |
| **Programming Language** | Python 3.11+                                       | Modern, robust, and possesses a rich ecosystem for rapid and secure development. |
| **Backend Framework** | Django 5.0+                                        | "Batteries-included" framework providing built-in security, ORM, and admin.      |
| **Database** | PostgreSQL 15+                                     | Powerful ORDBMS ensuring data integrity, ACID transactions, and complex queries. |
| **API Framework** | Django REST Framework (DRF)                        | The industry standard for building secure and scalable RESTful APIs in Django.   |
| **Frontend** | Bootstrap 5 & HTMX                                 | A modern combination for building fast, reactive interfaces with minimal JS.     |
| **Async Tasks** | Celery & Redis                                     | A standard, reliable stack for processing long-running tasks in the background.  |
| **Containerization** | Docker & Docker Compose                            | To unify development/production environments and simplify deployment.            |
| **Web Server** | Gunicorn                                           | A production-ready WSGI server designed for performance and concurrency.         |

## Getting Started

### Prerequisites

* Docker
* Docker Compose

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-repo/EduFlow-AcademySuite.git](https://github.com/your-repo/EduFlow-AcademySuite.git)
    cd EduFlow-AcademySuite
    ```

2.  **Create the environment file:**
    Duplicate the example environment file and customize it with your secret keys and settings.
    ```bash
    cp .env.example .env
    ```
    *Note: Fill in the `SECRET_KEY`, database credentials, and other required variables in the `.env` file.*

3.  **Build and run the services using Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    This command will build the Docker images and start the `web`, `db`, and `redis` services.

4.  **Apply database migrations:**
    In a separate terminal, run the following command to create the database schema:
    ```bash
    docker-compose exec web python manage.py migrate
    ```

5.  **Create a superuser:**
    To access the Django admin interface, create a superuser account:
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

6.  **Access the application:**
    The application should now be running at `http://localhost:8000`. The Django admin panel is available at `http://localhost:8000/admin`.

---

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.