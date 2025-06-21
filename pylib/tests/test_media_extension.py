import os
import pytest

from .shared import getEmptyCol
from anki.media import MediaManager
from anki.collection import Collection


@pytest.fixture
def media_manager():
    """Fixture que cria um MediaManager isolado para testes"""
    col = Collection(os.devnull)  # Coleção vazia em memória
    return MediaManager(col=col, server=False)

class TestExtensionFromMime:
    """Test cases for MIME-based extension handling"""
    
    def test_no_extension_valid_mime(self):
        """CT1: File without extension + valid MIME should get correct extension"""
        col = getEmptyCol()
        assert col.media.add_extension_based_on_mime("audio", "audio/mpeg") == "audio.mp3"
    
    def test_no_extension_invalid_mime(self):
        """CT2: File without extension + unknown MIME should remain unchanged"""
        col = getEmptyCol()
        assert col.media.add_extension_based_on_mime("file", "application/unknown") == "file"
    
    def test_with_extension_valid_mime(self):
        """CT3: File with existing extension should ignore MIME type"""
        col = getEmptyCol()
        assert col.media.add_extension_based_on_mime("image.png", "image/jpeg") == "image.png"

    def test_dotted_name_no_extension(self):
        """CT5: Filename with dots but no valid extension should get MIME extension"""
        col = getEmptyCol()
        assert col.media.add_extension_based_on_mime("version.2", "image/png") == "version.2.png"
    
    @pytest.mark.parametrize("mime,ext", [
        ("audio/mpeg", ".mp3"),
        ("image/jpeg", ".jpg"),
        ("image/avif", ".avif")
    ])
    def test_mime_type_mappings(self, mime, ext):
        """Parameterized test for multiple MIME type mappings"""
        col = getEmptyCol()
        assert col.media.add_extension_based_on_mime("file", mime) == f"file{ext}"
