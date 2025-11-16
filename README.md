# 🚀 Pin People Project

## 💡 Overview
This project is a Django-based portfolio application that extends the default Django user system to include detailed user profiles and location-based features. The application allows users to manage their own profile information and view all registered users on an interactive world map.

✨ Key Features
* Extended User Profiles
Includes home address, phone number, and geographic location (point geometry)

* Profile Management
Users can view and edit their own profile but cannot access other user profiles

* Full-Screen User Map
Displays all users’ locations on an interactive Leaflet map.
Clicking a marker shows the user’s location and link to the user's profile in a popup

* Authentication Rules
  * Regular users can access only their own profile on the main site
  * Superusers have full access to the admin interface and can view all user profiles on the main site


---

## 📌 Requirements

### Software on your machine

| Requirement | Version |
|------------|---------|
| Python | 3.10+ |
| Ansible | 2.12+ |
| Git | any |

> **⚠ IMPORTANT:**
> Docker must already be installed and running on the target machine.
> The playbook does **not** install Docker.
> If Docker is missing, install it using the official guide:
> [Install Docker](https://docs.docker.com/engine/install/)

Install Ansible if needed:

```sh
pip install ansible
```
---

## ⚙ Configure Deployment (vars.yml)

All important deployment settings are stored in vars.yml.  Edit the file before running the playbook to match your project setup:

```sh
vi vars.yml
```

## ▶️  Run Deployment

Once vars.yml is configured, run the playbook with:

```sh
ansible-playbook -i inventory deploy.yml -e @vars.yml --ask-become-pass
```

## 🛑 Stop Development Server and Cleanup

If you want to stop the development server and remove the PostgreSQL Docker container created by the deployment, run:

```sh
ansible-playbook -i inventory cleanup.yml -e @vars.yml --ask-become-pass
```

---
## 🔑 Access the Application

Login page
👉 http://127.0.0.1/


Superuser
```
Username: admin

Password: mySuperSecret
```


Regular user
```
Username: luna_moon

Password: mySecret!
```

Admin site
👉 http://127.0.0.1/admin/
```
Username: admin

Password: mySuperSecret
```

## 📊 View User Login Activity

Open Admin Dashboard:
👉 http://127.0.0.1/admin/
```
Username: admin

Password: mySuperSecret
```

In the sidebar, click “Log entries”

On the right, use the Filter menu and select:

Login

or Logout

This allows you to track every login/logout event across all users.
