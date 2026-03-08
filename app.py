from flask import Flask, render_template, request, redirect, url_for, session, abort, jsonify

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ---------------- USERS ----------------
users = {}

# ---------------- COURSES ----------------
courses = [
    {
        "id": "startup-basics",
        "title": "Startup Basics",
        "description": "Learn the fundamentals of starting a business.",
        "theory": """Startups are innovative businesses created to solve real-world problems using technology, creativity, and new business models.
Unlike traditional businesses, startups aim for rapid growth and scalability.
Most successful startups begin by identifying a specific problem faced by customers and designing a solution that adds value.
The first step in the startup journey is idea validation. Entrepreneurs must verify whether their idea truly solves a real problem and whether customers are willing to use or pay for the solution.
This stage often includes market research, competitor analysis, and discussions with potential users.
Once an idea is validated, founders develop a business model explaining how the startup will generate revenue.
Startups usually begin with small teams and limited resources, so founders must focus on efficiency and learning quickly from feedback.""",
        "questions": [
            {"q": "What is the first step in the startup journey?",
             "options": ["Idea Validation", "Hiring Employees", "Marketing", "Sales"],
             "answer": "Idea Validation"},
            {"q": "What is key during early stage of a startup?",
             "options": ["Customer Problem", "Brand Logo", "Office Location", "Website Design"],
             "answer": "Customer Problem"}
        ]
    },
    {
        "id": "funding-for-startups",
        "title": "Funding for Startups",
        "description": "Understand different funding options.",
        "theory": """Funding provides financial resources required to build, launch, and grow a startup.
In the early stages, many founders rely on bootstrapping, using personal savings or funds from friends and family.
After developing a prototype, startups often approach angel investors who provide money in exchange for equity.
Angel investors also offer mentorship and industry connections to founders.
As the startup grows, it may seek venture capital investments which are larger and support scalable business models.
Governments and startup ecosystems provide grants, incubators, and accelerator programs to support startups.
To secure funding, entrepreneurs usually prepare a pitch deck explaining problem, solution, business model, and market potential.""",
        "questions": [
            {"q": "Which is a common funding source for startups?",
             "options": ["Angel Investors", "Teachers", "Students", "Drivers"],
             "answer": "Angel Investors"},
            {"q": "What does bootstrapping mean?",
             "options": ["Using personal funds", "Seeking VC funding", "Taking loans", "Hiring staff"],
             "answer": "Using personal funds"}
        ]
    },
    {
        "id": "digital-marketing",
        "title": "Digital Marketing",
        "description": "Promote your startup online.",
        "theory": """Digital marketing is the practice of promoting products or services online to reach a large audience.
Startups use SEO to rank higher in search engine results and increase visibility.
Social media marketing is important, using platforms like LinkedIn, Instagram, and Facebook.
Content marketing helps attract potential customers through blogs, videos, and educational content.
Email marketing and paid ads are additional strategies to engage customers and generate leads.
Marketing analytics tools allow startups to track performance and improve campaigns.
Effective digital marketing is essential for startups to grow their customer base efficiently.""",
        "questions": [
            {"q": "What does SEO stand for?",
             "options": ["Search Engine Optimization", "System Engine Output", "Search Energy Output", "Software Engine Output"],
             "answer": "Search Engine Optimization"},
            {"q": "Which platform is best for B2B marketing?",
             "options": ["LinkedIn", "Instagram", "Snapchat", "Pinterest"],
             "answer": "LinkedIn"}
        ]
    },
    {
        "id": "product-management",
        "title": "Product Management",
        "description": "Learn product planning and roadmap.",
        "theory": """Product management involves planning, developing, and improving products that solve customer problems.
The product manager defines product vision and ensures the team delivers value.
A product roadmap outlines future features and improvements for the product.
Agile development allows iterative releases and feedback-driven improvements.
Understanding user needs and analyzing product performance are key responsibilities.
Product managers collaborate with designers, engineers, and marketing teams.
Continuous improvement ensures the product meets customer expectations and market demands.""",
        "questions": [
            {"q": "Which development model supports iteration?",
             "options": ["Agile", "Linear", "Static", "Waterfall"],
             "answer": "Agile"},
            {"q": "What is the purpose of a product roadmap?",
             "options": ["Plan features over time", "Hire developers", "Create logos", "Run ads"],
             "answer": "Plan features over time"}
        ]
    },
    {
        "id": "startup-finance",
        "title": "Startup Finance",
        "description": "Learn startup budgeting and financial planning.",
        "theory": """Financial management helps startups track income, expenses, and investments.
Startups must manage cash flow to pay employees, suppliers, and operational costs.
Budgeting allows efficient allocation of resources and prevents overspending.
Accounting and financial reporting help founders understand business performance.
Planning finances increases investor confidence and sustainability.
Startups may also plan for fundraising rounds and investor pitches.
Monitoring finances regularly is critical for long-term business success.""",
        "questions": [
            {"q": "What manages money movement?",
             "options": ["Cash Flow", "Planning", "Strategy", "Promotion"],
             "answer": "Cash Flow"},
            {"q": "Why is budgeting important?",
             "options": ["Avoid overspending", "Hire more staff", "Run ads", "Ignore investors"],
             "answer": "Avoid overspending"}
        ]
    },
    {
        "id": "startup-legal",
        "title": "Startup Legal",
        "description": "Legal basics for startups.",
        "theory": """Legal knowledge is essential for startups to operate responsibly and protect assets.
Choosing the right business structure, like private limited or partnership, is important.
Intellectual property rights, including patents and trademarks, protect innovations.
Legal agreements define responsibilities between founders, employees, and partners.
Compliance with tax regulations, licenses, and government policies is required.
Understanding contracts and agreements avoids future conflicts.
Following legal processes builds trust with investors, partners, and customers.""",
        "questions": [
            {"q": "What protects inventions?",
             "options": ["Intellectual Property", "License", "Certificate", "Contract"],
             "answer": "Intellectual Property"},
            {"q": "Which business structure is common for startups?",
             "options": ["Private Limited", "NGO", "Partnership", "Sole Proprietorship"],
             "answer": "Private Limited"}
        ]
    }
]

# ---------------- FUNDING ----------------
featured_funding = [
    {"title":"Startup India Seed Fund","sector":"Technology","description":"Seed funding for innovative startups.","amount":50},
    {"title":"Atal Innovation Mission","sector":"Innovation","description":"Innovation grants.","amount":75},
    {"title":"Digital India Grant","sector":"IT","description":"Funding for digital startups.","amount":100},
    {"title":"Stand Up India Loan","sector":"Women","description":"Loans for women entrepreneurs.","amount":200},
    {"title":"Pradhan Mantri Mudra Yojana","sector":"Finance","description":"Loans for micro enterprises.","amount":30},
    {"title":"National SC/ST Hub","sector":"Entrepreneurship","description":"Support for SC/ST entrepreneurs.","amount":40}
]

# ---------------- SCHEMES ----------------
schemes_list = [
    {"title":"Startup India Scheme","sector":"Technology","description":"Support for innovative startups","benefits":"Funding, mentorship, incubation","eligibility":"All startups","status":"Ongoing"},
    {"title":"Stand Up India","sector":"Women","description":"Loans for women entrepreneurs","benefits":"Loans up to ₹1 Cr","eligibility":"Women entrepreneurs","status":"Ongoing"},
    {"title":"Atal Innovation Mission","sector":"Innovation","description":"Promotes innovative startups","benefits":"Grants, mentorship, networking","eligibility":"Startups under 5 years","status":"Ongoing"},
    {"title":"Digital India Scheme","sector":"Digital","description":"Supports digital startups","benefits":"Funding, infrastructure support","eligibility":"Startups in IT sector","status":"Ongoing"},
    {"title":"Pradhan Mantri Mudra Yojana","sector":"Finance","description":"Loans for micro enterprises","benefits":"Loans up to ₹10 Lakh","eligibility":"Micro enterprises","status":"Ongoing"},
    {"title":"National SC/ST Hub","sector":"Entrepreneurship","description":"Support for SC/ST entrepreneurs","benefits":"Funding, mentorship, networking","eligibility":"SC/ST entrepreneurs","status":"Ongoing"}
]

# ---------------- HOME ----------------
@app.route("/")
def index():
    stats = {
        "registered":"12,450+",
        "funding":"₹8,200 Cr",
        "investors":"1,350+",
        "states":"36"
    }
    return render_template("index.html", stats=stats, home_cards=courses, username=session.get("user"))

# ---------------- LEARNING ----------------
@app.route("/learning")
def learning():
    return render_template("learning.html", courses=courses)

@app.route("/learning/<course_id>", methods=["GET","POST"])
def course_detail(course_id):
    course = next((c for c in courses if c["id"] == course_id), None)
    if not course:
        abort(404)
    score = None
    if request.method=="POST":
        score = 0
        for idx, q in enumerate(course["questions"]):
            if request.form.get(f"q{idx}") == q["answer"]:
                score += 1
    return render_template("course_detail.html", course=course, score=score)

# ---------------- REST OF THE APP ----------------
@app.route("/entrepreneurs")
def entrepreneurs():
    return render_template("entrepreneurs.html")

@app.route("/funding")
def funding():
    return render_template("funding.html", featured_funding=featured_funding)

@app.route("/submit-application", methods=["POST"])
def submit_application():
    name = request.form.get("name")
    email = request.form.get("email")
    startup = request.form.get("startup")
    description = request.form.get("description")
    funding_title = request.form.get("funding_title")
    print(f"Application Submitted: {funding_title}, {name}, {email}, {startup}, {description}")
    message = f"Your application for '{funding_title}' has been submitted successfully!"
    return render_template("funding.html", featured_funding=featured_funding, message=message)

@app.route("/schemes")
def schemes():
    return render_template("schemes.html", schemes_list=schemes_list)

@app.route("/ai-match")
def ai_match():
    return render_template("ai_match.html")

@app.route("/match-idea", methods=["POST"])
def match_idea():
    data = request.get_json()
    idea = data.get("idea","").lower()
    matched = []
    for funding in featured_funding:
        if "tech" in idea or "software" in idea:
            matched.append(funding)
    if not matched:
        matched = featured_funding[:2]
    return jsonify(matched)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if email in users and users[email]["password"]==password:
            session["user"] = users[email]["name"]
            return redirect(url_for("index"))
        return render_template("login.html", message="Invalid Email or Password")
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        if email in users:
            return render_template("register.html", message="Email already registered")
        users[email] = {"name":name,"password":password}
        session["user"] = name
        return redirect(url_for("index"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

# ---------------- RUN ----------------
if __name__=="__main__":
    app.run(debug=True)