import logging
import json
from django.db.models import F, Value, CharField
from django.db.models.functions import Concat
from collections import OrderedDict
import unicodedata

log = logging.getLogger(__name__)


class SerbianCyrillicSort:
    """
    Serbian Cyrillic alphabet ordering with custom case sensitivity.
    Case only matters when all characters are identical (lowercase before uppercase).
    """

    # Serbian Cyrillic alphabet order (base letters only, without case distinction)
    CYRILLIC_BASE_ORDER = {
        'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4, 'ђ': 5, 'е': 6, 'ж': 7,
        'з': 8, 'и': 9, 'ј': 10, 'к': 11, 'л': 12, 'љ': 13, 'м': 14,
        'н': 15, 'њ': 16, 'о': 17, 'п': 18, 'р': 19, 'с': 20, 'т': 21,
        'ћ': 22, 'у': 23, 'ф': 24, 'х': 25, 'ц': 26, 'ч': 27, 'џ': 28, 'ш': 29,
    }

    # Latin to Cyrillic transliteration map (Serbian)
    LATIN_TO_CYRILLIC = {
        'a': 'а', 'A': 'А',
        'b': 'б', 'B': 'Б',
        'c': 'ц', 'C': 'Ц',
        'd': 'д', 'D': 'Д',
        'e': 'е', 'E': 'Е',
        'f': 'ф', 'F': 'Ф',
        'g': 'г', 'G': 'Г',
        'h': 'х', 'H': 'Х',
        'i': 'и', 'I': 'И',
        'j': 'ј', 'J': 'Ј',
        'k': 'к', 'K': 'К',
        'l': 'л', 'L': 'Л',
        'm': 'м', 'M': 'М',
        'n': 'н', 'N': 'Н',
        'o': 'о', 'O': 'О',
        'p': 'п', 'P': 'П',
        'r': 'р', 'R': 'Р',
        's': 'с', 'S': 'С',
        't': 'т', 'T': 'Т',
        'u': 'у', 'U': 'У',
        'v': 'в', 'V': 'В',
        'z': 'з', 'Z': 'З',
        # Digraphs
        'č': 'ч', 'Č': 'Ч',
        'ć': 'ћ', 'Ć': 'Ћ',
        'đ': 'ђ', 'Đ': 'Ђ',
        'dž': 'џ', 'Dž': 'Џ', 'DŽ': 'Џ',
        'lj': 'љ', 'Lj': 'Љ', 'LJ': 'Љ',
        'nj': 'њ', 'Nj': 'Њ', 'NJ': 'Њ',
        'š': 'ш', 'Š': 'Ш',
        'ž': 'ж', 'Ž': 'Ж',
    }

    # Ordered list of Cyrillic letters for grouping (lowercase only)
    ALPHABET_ORDER = ['а', 'б', 'в', 'г', 'д', 'ђ', 'е', 'ж', 'з', 'и', 'ј',
                      'к', 'л', 'љ', 'м', 'н', 'њ', 'о', 'п', 'р', 'с', 'т',
                      'ћ', 'у', 'ф', 'х', 'ц', 'ч', 'џ', 'ш']

    # Non-Serbian Latin letters that get their own groups (at the end)
    NON_SERBIAN_LETTERS = ['q', 'w', 'x', 'y']

    @classmethod
    def remove_combining_marks(cls, text):
        """
        Remove all combining diacritical marks from the text.
        Uses Unicode normalization (NFD) to decompose characters,
        then filters out combining marks.

        Args:
            text: Input string

        Returns:
            String with combining marks removed
        """
        if not text:
            return ''

        # Normalize to NFD (decomposed form)
        normalized = unicodedata.normalize('NFD', text)

        # Filter out combining characters (category 'Mn' = Mark, nonspacing)
        without_marks = ''.join(
            char for char in normalized
            if unicodedata.category(char) != 'Mn'
        )

        return without_marks

    @classmethod
    def transliterate_to_cyrillic(cls, text):
        """
        Transliterate Latin characters to Serbian Cyrillic.
        Handles multi-character digraphs (dž, lj, nj).
        """
        if not text:
            return ''

        result = []
        i = 0
        while i < len(text):
            # Try three-character match first (for DŽ, LJ, NJ)
            if i + 2 < len(text):
                three_char = text[i:i+3]
                if three_char in cls.LATIN_TO_CYRILLIC:
                    result.append(cls.LATIN_TO_CYRILLIC[three_char])
                    i += 3
                    continue

            # Try two-character match (for dž, lj, nj, etc.)
            if i + 1 < len(text):
                two_char = text[i:i+2]
                if two_char in cls.LATIN_TO_CYRILLIC:
                    result.append(cls.LATIN_TO_CYRILLIC[two_char])
                    i += 2
                    continue

            # Single character
            char = text[i]
            result.append(cls.LATIN_TO_CYRILLIC.get(char, char))
            i += 1

        return ''.join(result)

    @classmethod
    def remove_punctuation(cls, text):
        """
        Remove punctuation characters from the text.
        """
        if not text:
            return ''

        return text.replace('.', '').replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        # return ''.join(
        #     char for char in text
        #     if not unicodedata.category(char).startswith('P')
        # )

    @classmethod
    def get_sort_key(cls, text):
        """
        Generate a sort key for the given text.
        Returns a tuple of (character_keys, case_key) for comparison.

        The sorting works in two levels:
        1. Primary: Compare characters case-insensitively by alphabet order
        2. Secondary: If all characters are identical, lowercase comes before uppercase

        Process:
        1. Remove combining diacritical marks
        2. Transliterate to Cyrillic
        3. Convert to numeric sort key (case-insensitive)
        4. Add case information as tiebreaker
        """
        if not text:
            return (tuple(), tuple())

        # Remove combining marks first
        text_without_marks = cls.remove_combining_marks(text)

        # Transliterate to Cyrillic
        cleaned_text = cls.remove_punctuation(text_without_marks)
        cyrillic_text = cls.transliterate_to_cyrillic(cleaned_text)

        # Convert to sort key based on alphabet order (case-insensitive)
        primary_key = []
        case_key = []

        for char in cyrillic_text:
            char_lower = char.lower()

            if char_lower in cls.CYRILLIC_BASE_ORDER:
                # Use base letter order for primary sorting
                primary_key.append(cls.CYRILLIC_BASE_ORDER[char_lower])
                # Track case: 0 for lowercase, 1 for uppercase (lowercase comes first)
                case_key.append(0 if char.islower() else 1)
            else:
                # For characters not in the alphabet, use Unicode codepoint
                # Add a large offset to place them after the alphabet
                primary_key.append(10000 + ord(char_lower))
                case_key.append(0 if char.islower() else 1)

        # Return tuple: primary key (case-insensitive), then case key (tiebreaker)
        return (tuple(primary_key), tuple(case_key))

    @classmethod
    def get_combined_sort_key(cls, text_value, ordinal_value):
        """
        Generate a combined sort key for text and ordinal fields.
        Text field has higher priority, ordinal field has lower priority.

        Args:
            text_value: String value to sort by (primary)
            ordinal_value: Integer ordinal number (secondary)

        Returns:
            Tuple combining text sort key and ordinal value
        """
        text_key = cls.get_sort_key(text_value)
        # Handle None values for ordinal - place them at the end
        ordinal_key = ordinal_value if ordinal_value is not None else float('-inf')

        # Combine: text key first (primary, secondary), then ordinal (tertiary)
        return text_key + (ordinal_key,)

    @classmethod
    def get_first_letter_for_grouping(cls, text):
        """
        Get the first letter of the original text for grouping purposes.

        ## This method does NOT transliterate - it keeps the original letter.
        This allows q, w, x, y to have their own groups.

        Args:
            text: Input string

        Returns:
            Single character string (lowercase letter or '#')
        """
        if not text:
            return '#'

        # Remove combining marks
        text_without_marks = cls.remove_combining_marks(text)
        text_without_marks = cls.remove_punctuation(text_without_marks)
        text_without_marks = cls.transliterate_to_cyrillic(text_without_marks)

        if not text_without_marks:
            return '#'

        # Get first character and convert to lowercase
        first_char = text_without_marks[0].lower()

        # Check if it's a letter
        if first_char.isalpha():
            return first_char
        else:
            # Non-letter characters go to '#'
            return '#'

    @classmethod
    def get_group_display_letter(cls, letter):
        """
        Get the display version of a grouping letter.

        For Cyrillic letters, returns uppercase Cyrillic.
        For Latin letters, returns uppercase Latin.
        For special chars, returns '#'.

        Args:
            letter: Lowercase letter or '#'

        Returns:
            Uppercase display letter
        """
        if letter == '#':
            return '#'

        # Check if it's a Latin letter that needs transliteration for display
        if letter in cls.LATIN_TO_CYRILLIC:
            # Transliterate to Cyrillic for display
            cyrillic = cls.LATIN_TO_CYRILLIC[letter]
            return cyrillic.upper()

        # For non-Serbian Latin letters (q, w, x, y), keep them as Latin uppercase
        return letter.upper()

    @classmethod
    def get_letter_sort_key(cls, letter):
        """
        Get the sort key for a letter group.

        Order:
        1. Serbian Cyrillic letters (in alphabet order)
        2. Non-Serbian Latin letters: q, w, x, y (in this order)
        3. Special characters '#'

        Args:
            letter: Single lowercase character or '#'

        Returns:
            Integer sort key
        """
        # Check if it's a Serbian letter (Latin or Cyrillic)
        if letter in cls.LATIN_TO_CYRILLIC:
            # Transliterate and get position in Cyrillic alphabet
            cyrillic = cls.LATIN_TO_CYRILLIC[letter].lower()
            if cyrillic in cls.CYRILLIC_BASE_ORDER:
                return cls.CYRILLIC_BASE_ORDER[cyrillic]

        # Check if it's already Cyrillic
        if letter in cls.CYRILLIC_BASE_ORDER:
            return cls.CYRILLIC_BASE_ORDER[letter]

        # Non-Serbian Latin letters come after Serbian alphabet
        if letter in cls.NON_SERBIAN_LETTERS:
            base_index = len(cls.CYRILLIC_BASE_ORDER)
            return base_index + cls.NON_SERBIAN_LETTERS.index(letter)

        # Everything else (including '#') comes at the very end
        return len(cls.CYRILLIC_BASE_ORDER) + len(cls.NON_SERBIAN_LETTERS) + ord(letter)

    @classmethod
    def sort_queryset(cls, queryset, text_field_name, ordinal_field_name=None):
        """
        Sort a Django queryset by the specified fields using Serbian Cyrillic rules.

        Args:
            queryset: Django QuerySet to sort
            text_field_name: Name of the text field to sort by (primary)
            ordinal_field_name: Name of the integer ordinal field (secondary, optional)

        Returns:
            Sorted list of model instances
        """
        # Fetch all items from queryset
        items = list(queryset)

        # Sort using the appropriate key
        if ordinal_field_name:
            items.sort(key=lambda obj: cls.get_combined_sort_key(
                getattr(obj, text_field_name, ''),
                getattr(obj, ordinal_field_name, None)
            ))
        else:
            items.sort(key=lambda obj: cls.get_sort_key(
                getattr(obj, text_field_name, '')
            ))

        return items

    @classmethod
    def group_by_first_letter(cls, queryset, text_field_name, ordinal_field_name=None):
        """
        Sort and group queryset items by the first letter of the text field.

        Returns an OrderedDict where:
        - Keys are uppercase display letters (А, Б, В, ..., Q, W, X, Y, #)
        - Values are lists of items starting with that letter
        - Groups are ordered: Serbian Cyrillic alphabet, then Q, W, X, Y, then #
        - Items within each group maintain sort order

        Args:
            queryset: Django QuerySet to sort and group
            text_field_name: Name of the text field to sort by
            ordinal_field_name: Name of the integer ordinal field (optional)

        Returns:
            OrderedDict of {letter: [items]} maintaining sort order
        """
        # First, sort the queryset
        sorted_items = cls.sort_queryset(queryset, text_field_name, ordinal_field_name)

        # Create groups dictionary
        groups = {}

        for item in sorted_items:
            text_value = getattr(item, text_field_name, '')
            first_letter = cls.get_first_letter_for_grouping(text_value)

            if first_letter not in groups:
                groups[first_letter] = []

            groups[first_letter].append(item)
        log.info(f'groups["а"]: {json.dumps(groups["а"], indent=2, default=str)}')

        # Sort groups by letter order and create OrderedDict
        sorted_groups = OrderedDict()
        sorted_letters = sorted(groups.keys(), key=cls.get_letter_sort_key)
        log.info(f'sorted_letters: {json.dumps(sorted_letters, indent=2, default=str)}')
        for letter in sorted_letters:
            # Get the display version of the letter
            display_letter = cls.get_group_display_letter(letter)
            sorted_groups[display_letter] = groups[letter]
        log.info(f'sorted_groups["а"]: {json.dumps(sorted_groups["А"], indent=2, default=str)}')

        return sorted_groups


# Usage examples
def get_sorted_items(queryset, text_field='name', ordinal_field=None):
    """
    Get items sorted by Serbian Cyrillic alphabet rules with optional ordinal field.

    Examples:
        # Sort by text field only
        queryset = MyModel.objects.filter(active=True)
        sorted_items = get_sorted_items(queryset, 'name')

        # Sort by text field (primary) and ordinal field (secondary)
        sorted_items = get_sorted_items(queryset, 'name', 'order')
    """
    return SerbianCyrillicSort.sort_queryset(queryset, text_field, ordinal_field)


def get_grouped_items(queryset, text_field='name', ordinal_field=None):
    """
    Get items grouped by first letter and sorted within each group.

    Returns an OrderedDict where keys are uppercase letters (А, Б, В, ..., Q, W, X, Y, #)
    and values are lists of items starting with that letter.

    Examples:
        # Group by text field only
        queryset = MyModel.objects.filter(active=True)
        grouped_items = get_grouped_items(queryset, 'name')

        # Access groups:
        for letter, items in grouped_items.items():
            print(f"{letter}: {len(items)} items")
            for item in items:
                print(f"  - {item.name}")

        # Group by text field (primary) and ordinal field (secondary)
        grouped_items = get_grouped_items(queryset, 'name', 'order')
    """
    return SerbianCyrillicSort.group_by_first_letter(queryset, text_field, ordinal_field)
