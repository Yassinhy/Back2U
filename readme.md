# Back2U
 
A lost-and-found web app. Finders upload items they've found along with verification questions; claimants answer those questions to prove ownership, and answers are scored using the Gemini API to help finders decide who to return the item to.
 
## Features
 
- User registration and login
- Upload found items with a photo, description, and location
- Optional image filters (grayscale, blur) on upload
- Claimants submit answers to verification questions
- AI-assisted scoring of claim answers via Gemini
- View and manage your own uploads and incoming claims
## Tech Stack
 
- **Backend:** Flask
- **Database:** SQLite (via `cs50`)
- **Sessions:** Flask-Session (filesystem)
- **Forms:** Flask-WTF
- **Image uploads:** Flask-Uploads + Pillow
- **AI scoring:** Google Gemini (`google-genai`)


# How to Use Back2U
 
## 1. Create an Account
- Go to the **Register** page.
- Enter your email, phone number, and a password.
- Log in with your new account.
## 2. Found Something?
- Click **Found an Item**.
- Upload a photo of the item.
- Add a title, location, and description.
- Write 2–3 verification questions only the real owner would know the answer to (e.g. "What's inside the bag?").
- Submit — your item is now listed for others to see.
## 3. Lost Something?
- Browse the items on the home page.
- Find one that matches what you lost and open it.
- Answer the owner's verification questions as accurately as you can.
- Submit your answers — they'll be reviewed by the finder.
## 4. Reviewing Claims
- Go to **My Uploads** to see items you've posted.
- Open an item to see everyone who claimed it, along with an AI-generated confidence score for each answer.
- Contact the person with the strongest match to arrange the return.
## Tips
- The more specific your verification questions, the harder it is for someone to fake a claim.
- Confidence scores are a guide, not a guarantee — use your own judgment too.