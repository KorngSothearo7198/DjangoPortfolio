

from django.db import models

#================================

# hero Model

# Profile 

class Profile(models.Model):
    full_name = models.CharField(max_length=100)
    short_title = models.CharField(max_length=100)  # Software Engineer
    description = models.TextField()

    profile_image = models.ImageField(upload_to='profile/')
    cv_file = models.FileField(upload_to='documents/', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Add timestamps
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

# Tech Stack (Used in Hero Section)

class TechStack(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='tech_stacks'
    )

    name = models.CharField(max_length=50)        # Django, JavaScript
    icon_class = models.CharField(max_length=50) # fab fa-python
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    

# about 

# What I Do / Services
class Service(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="services")
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_class = models.CharField(max_length=100, help_text="FontAwesome icon class, e.g., fas fa-laptop-code")
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']


# Timeline / Journey
class Journey(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="journeys")
    year = models.CharField(max_length=10)
    title = models.CharField(max_length=150, blank=True)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.year} - {self.title}"

    class Meta:
        ordering = ['order']



# Skill Category (Technical / Professional / Tools)


class SkillCategory(models.Model):
    name = models.CharField(max_length=50)  
    # Example: Technical Skills, Professional Skills, Tools & Technologies

    slug = models.SlugField(unique=True)  
    # technical, professional, tools

    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


# Main Skill (Skill Card)

class Skill(models.Model):
    profile = models.ForeignKey(
        "Profile",
        on_delete=models.CASCADE,
        related_name="skills"
    )

    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.CASCADE,
        related_name="skills"
    )

    title = models.CharField(max_length=100)  
    # Python & Django, Problem Solving

    icon_class = models.CharField(max_length=50)  
    # fab fa-python, fas fa-lightbulb

    level_text = models.CharField(max_length=50)  
    # Advanced, Intermediate

    progress_percent = models.PositiveIntegerField()  
    # 90, 75, 60

    description = models.TextField()

    years_experience = models.CharField(max_length=50)  
    # 2+ Years Experience

    project_count = models.CharField(max_length=50)  
    # 3+ Projects, 15+ Designs

    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

# Skill Tags (Django REST, Flutter, SQL)


class SkillTag(models.Model):
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="tags"
    )

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Professional Skill Breakdown (Bars inside card)

class SkillBreakdown(models.Model):
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="breakdowns"
    )

    name = models.CharField(max_length=100)  
    # Analytical Thinking

    percent = models.PositiveIntegerField()  
    # 80

    def __str__(self):
        return f"{self.skill.title} - {self.name}"


# Tool Category (Development Tools, Languages, Design)

class ToolCategory(models.Model):
    name = models.CharField(max_length=100)  # Development Tools, Programming Languages
    icon_class = models.CharField(max_length=50)  # e.g., "fas fa-code", "fas fa-keyboard" 
    order = models.PositiveIntegerField(default=0)  # For ordering in template

    def __str__(self):
        return self.name


# Tool / Technology Item

class Tool(models.Model):
    profile = models.ForeignKey(
        "Profile",
        on_delete=models.CASCADE,
        related_name="tools"
    )

    category = models.ForeignKey(
        ToolCategory,
        on_delete=models.CASCADE,
        related_name="tools"
    )

    name = models.CharField(max_length=50)   # GitHub, VS Code, Python, Figma, etc.
    icon_class = models.CharField(max_length=50)  # "fab fa-github", "fas fa-terminal", "fab fa-python"

    def __str__(self):
        return self.name



# Project Category (Filter Buttons)

class ProjectCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    icon_class = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


# Project (Main Card)

class Project(models.Model):
    profile = models.ForeignKey(
        "Profile",
        on_delete=models.CASCADE,
        related_name="projects"
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    image = models.ImageField(upload_to="projects/")

    year = models.PositiveIntegerField()
    duration = models.CharField(max_length=50)  
    # 4 Weeks, 6 Weeks

    category = models.ManyToManyField(
        ProjectCategory,
        related_name="projects"
    )

    badge_text = models.CharField(max_length=50, blank=True)  
    # Full Stack, Mobile/Android

    github_url = models.URLField(blank=True)
    live_demo_url = models.URLField(blank=True)
    details_url = models.URLField(blank=True)

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Project Tech Stack (CSS, Flutter, Firebase)

class ProjectTech(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="techs"
    )

    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.project.title} - {self.name}"



# Project Features (✔ Responsive, ✔ SEO)

class ProjectFeature(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="features"
    )

    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text


# (Optional) Project Link Type (Clean Admin)

class ProjectLink(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="links"
    )

    icon_class = models.CharField(max_length=50)
    url = models.URLField()
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title




# ContactMessage

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"
    
# ContactInfor

class ContactInfo(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    location = models.CharField(max_length=100)

    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    telegram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.email





# Chart Messager

# class ChatMessage(models.Model):
#     sender = models.CharField(max_length=50)  # 'user' or 'bot'
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.sender}: {self.message[:20]}"
    

class ChatMessage(models.Model):
    SENDER_CHOICES = [
        ('user', 'User'),
        ('bot', 'Bot'),
    ]
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.message[:20]}"