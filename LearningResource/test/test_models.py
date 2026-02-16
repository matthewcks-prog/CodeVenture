import pytest
from LearningResource.models import VideoTutorial, LearningModule, SubModule, Badge
from LearningResource import youtube_utils
from django.db import IntegrityError


# Fixtures
@pytest.fixture
def video_tutorial():
    return VideoTutorial.objects.create(name="Sample Video", video_id="rHux0gMZ3Eg")


@pytest.fixture
def learning_module():
    return LearningModule.objects.create(name="Django Basics", short_name="DJ-Basics", description="Intro to Django")


@pytest.fixture
def sub_module(video_tutorial, learning_module):
    return SubModule.objects.create(
        name="Setup",
        parent_module=learning_module,
        description="Setting up Django",
        video=video_tutorial,
    )


@pytest.fixture
def badge():
    return Badge.objects.create(
        name="Django Novice",
        icon_url="https://example.com/badge.png",
        description="Earned after completing Django Basics",
    )


# VideoTutorial Tests
@pytest.mark.django_db
def test_video_tutorial_creation(video_tutorial):
    assert VideoTutorial.objects.count() == 1
    assert video_tutorial.name == "Sample Video"
    assert len(video_tutorial.video_id) == 11
    assert video_tutorial.video_id == "rHux0gMZ3Eg"


@pytest.mark.django_db
def test_video_tutorial_embed_url(video_tutorial):
    """Model exposes a ready-to-use embed URL."""
    assert video_tutorial.embed_url == youtube_utils.build_embed_url("rHux0gMZ3Eg")


def test_youtube_utils_extracts_id_from_full_url():
    url = "https://www.youtube.com/watch?v=rHux0gMZ3Eg&ab_channel=Example"
    assert youtube_utils.extract_video_id(url) == "rHux0gMZ3Eg"


def test_youtube_utils_rejects_invalid_id():
    invalid = "not-a-valid-id"
    normalised = youtube_utils.extract_video_id(invalid)
    assert not youtube_utils.is_valid_video_id(normalised or "")


# LearningModule Tests
@pytest.mark.django_db
def test_learning_module_creation(learning_module):
    assert LearningModule.objects.count() == 1
    assert learning_module.name == "Django Basics"
    assert learning_module.short_name == "DJ-Basics"


@pytest.mark.django_db
def test_learning_module_name_uniqueness(learning_module):
    with pytest.raises(IntegrityError):
        LearningModule.objects.create(name="Django Basics", short_name="DJ-Advanced", description="Another Module")


@pytest.mark.django_db
def test_learning_module_thumbnail(learning_module):
    assert learning_module.thumbnail == ''  # Checking default value


# SubModule Tests
@pytest.mark.django_db
def test_sub_module_creation(sub_module):
    assert SubModule.objects.count() == 1
    assert sub_module.name == "Setup"
    assert sub_module.parent_module.name == "Django Basics"
    assert sub_module.difficulty_level == 'Basic'
    assert sub_module.video.name == "Sample Video"


@pytest.mark.django_db
def test_sub_module_relationships(learning_module, sub_module):
    assert learning_module.sub_modules.count() == 1
    assert learning_module.sub_modules.first().name == "Setup"


@pytest.mark.django_db
def test_sub_module_difficulty_choices(sub_module):
    assert sub_module.difficulty_level in dict(SubModule.DIFFICULTY_CHOICES).keys()


# Badge Tests
@pytest.mark.django_db
def test_badge_creation(badge):
    assert Badge.objects.count() == 1
    assert badge.name == "Django Novice"


@pytest.mark.django_db
def test_video_tutorial_str(video_tutorial):
    assert str(video_tutorial) == "Sample Video"


@pytest.mark.django_db
def test_learning_module_str(learning_module):
    assert str(learning_module) == "Django Basics"


@pytest.mark.django_db
def test_sub_module_str(sub_module):
    assert str(sub_module) == "DJ-Basics - Setup"


@pytest.mark.django_db
def test_learning_module_ordered_submodules(learning_module):
    """ordered_submodules follows prev/next chain when present."""
    v1 = VideoTutorial.objects.create(name="V1", video_id="11111111111")
    v2 = VideoTutorial.objects.create(name="V2", video_id="22222222222")
    s1 = SubModule.objects.create(
        name="First",
        parent_module=learning_module,
        description="First",
        video=v1,
        prev_submodule=None,
    )
    s2 = SubModule.objects.create(
        name="Second",
        parent_module=learning_module,
        description="Second",
        video=v2,
        prev_submodule=s1,
    )
    s1.next_submodule = s2
    s1.save()
    ordered = learning_module.ordered_submodules()
    assert [x.name for x in ordered] == ["First", "Second"]
