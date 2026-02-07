from django.contrib import admin
from .models import (
    ChatMessage, ContactInfo, Journey, Profile, Service, TechStack, SkillCategory, Skill, SkillTag, SkillBreakdown,
    ToolCategory, Tool,
    ProjectCategory, Project, ProjectTech, ProjectFeature, ProjectLink,
    ContactMessage
)

# ======== Inlines ========

class TechStackInline(admin.TabularInline):
    model = TechStack
    extra = 1

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1

class SkillTagInline(admin.TabularInline):
    model = SkillTag
    extra = 1

class SkillBreakdownInline(admin.TabularInline):
    model = SkillBreakdown
    extra = 1

class ToolInline(admin.TabularInline):
    model = Tool
    extra = 1

class ProjectTechInline(admin.TabularInline):
    model = ProjectTech
    extra = 1

class ProjectFeatureInline(admin.TabularInline):
    model = ProjectFeature
    extra = 1

class ProjectLinkInline(admin.TabularInline):
    model = ProjectLink
    extra = 1

# ======== Admin Classes ========

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "short_title", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("full_name", "short_title")
    inlines = [TechStackInline, SkillInline, ToolInline]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'profile', 'order')
    list_filter = ('profile',)
    ordering = ('profile', 'order')


@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'profile', 'order')
    list_filter = ('profile',)
    ordering = ('profile', 'order')

    


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    search_fields = ("name", "slug")

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("title", "profile", "category", "level_text", "progress_percent")
    list_filter = ("category", "level_text", "profile")
    search_fields = ("title",)

@admin.register(SkillTag)
class SkillTagAdmin(admin.ModelAdmin):
    list_display = ("name", "skill")
    search_fields = ("name", "skill__title")

@admin.register(SkillBreakdown)
class SkillBreakdownAdmin(admin.ModelAdmin):
    list_display = ("name", "percent", "skill")
    search_fields = ("name", "skill__title")

@admin.register(ToolCategory)
class ToolCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "icon_class", "order")
    search_fields = ("name",)

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "profile")
    list_filter = ("category", "profile")
    search_fields = ("name",)

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon_class")
    search_fields = ("name", "slug")

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "profile", "year", "badge_text", "is_active")
    list_filter = ("year", "is_active", "category")
    search_fields = ("title", "description")
    inlines = [ProjectTechInline, ProjectFeatureInline, ProjectLinkInline]

@admin.register(ProjectTech)
class ProjectTechAdmin(admin.ModelAdmin):
    list_display = ("name", "project")
    search_fields = ("name", "project__title")

@admin.register(ProjectFeature)
class ProjectFeatureAdmin(admin.ModelAdmin):
    list_display = ("text", "project")
    search_fields = ("text", "project__title")

@admin.register(ProjectLink)
class ProjectLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "project")
    search_fields = ("title", "project__title")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject')
    ordering = ('-created_at',)



admin.site.register(ContactInfo)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'message', 'created_at')
    ordering = ('-created_at',)






# from django.contrib import admin
# from .models import (
#     ChatMessage, ContactInfo, Profile, TechStack, SkillCategory, Skill, SkillTag, SkillBreakdown,
#     ToolCategory, Tool,
#     ProjectCategory, Project, ProjectTech, ProjectFeature, ProjectLink,
#     ContactMessage
# )

# # ======== Inlines ========

# class TechStackInline(admin.TabularInline):
#     model = TechStack
#     extra = 1

# class SkillInline(admin.TabularInline):
#     model = Skill
#     extra = 1

# class ToolInline(admin.TabularInline):
#     model = Tool
#     extra = 1

# class SkillTagInline(admin.TabularInline):
#     model = SkillTag
#     extra = 1

# class SkillBreakdownInline(admin.TabularInline):
#     model = SkillBreakdown
#     extra = 1

# class ProjectTechInline(admin.TabularInline):
#     model = ProjectTech
#     extra = 1

# class ProjectFeatureInline(admin.TabularInline):
#     model = ProjectFeature
#     extra = 1

# class ProjectLinkInline(admin.TabularInline):
#     model = ProjectLink
#     extra = 1


# # ======== Admin Classes ========

# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ("full_name", "short_title", "is_active", "created_at")
#     list_filter = ("is_active", "created_at")
#     search_fields = ("full_name", "short_title", "bio")
#     readonly_fields = ("created_at", "updated_at")
#     inlines = [TechStackInline, SkillInline, ToolInline]
#     fieldsets = (
#         ("Basic Info", {"fields": ("full_name", "short_title", "bio", "is_active")}),
#         ("Social Links", {"fields": ("github_url", "linkedin_url", "telegram_url", "facebook_url")}),
#     )


# @admin.register(SkillCategory)
# class SkillCategoryAdmin(admin.ModelAdmin):
#     list_display = ("name", "slug", "order")
#     search_fields = ("name", "slug")
#     ordering = ("order",)


# @admin.register(Skill)
# class SkillAdmin(admin.ModelAdmin):
#     list_display = ("title", "profile", "category", "level_text", "progress_percent")
#     list_filter = ("category", "level_text", "profile")
#     search_fields = ("title",)
#     inlines = [SkillTagInline, SkillBreakdownInline]


# @admin.register(ToolCategory)
# class ToolCategoryAdmin(admin.ModelAdmin):
#     list_display = ("name", "icon_class", "order")
#     search_fields = ("name",)
#     ordering = ("order",)


# @admin.register(Tool)
# class ToolAdmin(admin.ModelAdmin):
#     list_display = ("name", "category", "profile")
#     list_filter = ("category", "profile")
#     search_fields = ("name",)


# @admin.register(ProjectCategory)
# class ProjectCategoryAdmin(admin.ModelAdmin):
#     list_display = ("name", "slug", "icon_class")
#     search_fields = ("name", "slug")


# @admin.register(Project)
# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ("title", "profile", "year", "badge_text", "is_active")
#     list_filter = ("year", "is_active", "category")
#     search_fields = ("title", "description")
#     inlines = [ProjectTechInline, ProjectFeatureInline, ProjectLinkInline]
#     readonly_fields = ("created_at",)
#     fieldsets = (
#         ("Project Info", {"fields": ("title", "profile", "description", "year", "badge_text", "is_active")}),
#         ("Category & Tags", {"fields": ("category",)}),
#     )


# @admin.register(ContactMessage)
# class ContactMessageAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
#     list_filter = ('is_read', 'created_at')
#     search_fields = ('name', 'email', 'subject')
#     ordering = ('-created_at',)
#     readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')


# @admin.register(ChatMessage)
# class ChatMessageAdmin(admin.ModelAdmin):
#     list_display = ('sender', 'message', 'created_at')
#     ordering = ('-created_at',)
#     readonly_fields = ('sender', 'message', 'created_at')


# # Contact info singleton
# @admin.register(ContactInfo)
# class ContactInfoAdmin(admin.ModelAdmin):
#     list_display = ('email', 'phone', 'location', 'github_url', 'linkedin_url', 'telegram_url', 'facebook_url')
#     readonly_fields = ('created_at', 'updated_at')
