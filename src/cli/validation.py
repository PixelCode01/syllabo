import os
from typing import Dict, Any, Optional, Tuple, List

class InputValidator:
    """Validates and sanitizes CLI input arguments"""

    @staticmethod
    def validate_file_path(file_path: Optional[str]) -> Tuple[bool, str]:
        """Validate if a file path exists and is readable

        Args:
            file_path: Path to the file to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not file_path:
            return False, "No file path provided"

        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}"

        if not os.path.isfile(file_path):
            return False, f"Not a file: {file_path}"

        if not os.access(file_path, os.R_OK):
            return False, f"File not readable: {file_path}"

        return True, ""

    @staticmethod
    def validate_topic(topic: Optional[str]) -> Tuple[bool, str]:
        """Validate if a topic is provided and has reasonable length

        Args:
            topic: The topic string to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not topic:
            return False, "No topic provided"

        if len(topic.strip()) < 2:
            return False, "Topic is too short"

        if len(topic) > 200:
            return False, "Topic is too long (max 200 characters)"

        return True, ""

    @staticmethod
    def validate_positive_integer(value: Optional[int], name: str) -> Tuple[bool, str]:
        """Validate if a value is a positive integer

        Args:
            value: The integer value to validate
            name: Name of the parameter for error messages

        Returns:
            Tuple of (is_valid, error_message)
        """
        if value is None:
            return False, f"{name} not provided"

        if not isinstance(value, int):
            return False, f"{name} must be an integer"

        if value <= 0:
            return False, f"{name} must be positive"

        return True, ""

    @staticmethod
    def validate_export_format(format_type: str, supported_formats: List[str]) -> Tuple[bool, str]:
        """Validate if an export format is supported

        Args:
            format_type: The format type to validate
            supported_formats: List of supported format types

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not format_type:
            return False, "No export format provided"

        if format_type not in supported_formats:
            return False, f"Unsupported format: {format_type}. Supported formats: {', '.join(supported_formats)}"

        return True, ""

    @staticmethod
    def validate_analyze_args(args: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate arguments for the analyze command

        Args:
            args: The arguments to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Either file or text must be provided
        if not args.get('file') and not args.get('text'):
            return False, "Either --file or --text must be provided"

        # If file is provided, validate it
        if args.get('file'):
            is_valid, error = InputValidator.validate_file_path(args['file'])
            if not is_valid:
                return False, error

        # Validate max_videos if provided
        if args.get('max_videos'):
            is_valid, error = InputValidator.validate_positive_integer(args['max_videos'], 'max_videos')
            if not is_valid:
                return False, error

        # Validate export format if save is enabled
        if args.get('save') and args.get('export_format'):
            is_valid, error = InputValidator.validate_export_format(
                args['export_format'], 
                ['json', 'csv', 'markdown', 'html']
            )
            if not is_valid:
                return False, error

        return True, ""

    @staticmethod
    def validate_search_args(args: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate arguments for the search command

        Args:
            args: The arguments to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate topic
        is_valid, error = InputValidator.validate_topic(args.get('topic'))
        if not is_valid:
            return False, error

        # Validate max_videos if provided
        if args.get('max_videos'):
            is_valid, error = InputValidator.validate_positive_integer(args['max_videos'], 'max_videos')
            if not is_valid:
                return False, error

        # Validate export format if save is enabled
        if args.get('save') and args.get('export_format'):
            is_valid, error = InputValidator.validate_export_format(
                args['export_format'], 
                ['json', 'csv', 'markdown', 'html']
            )
            if not is_valid:
                return False, error

        return True, ""

    @staticmethod
    def validate_review_args(args: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate arguments for review commands

        Args:
            args: The arguments to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        action = args.get('review_action')

        # Different validations based on review action
        if action in ['add', 'mark', 'remove']:
            # Validate topic
            is_valid, error = InputValidator.validate_topic(args.get('topic'))
            if not is_valid:
                return False, error

        # No specific validations needed for other review actions

        return True, ""
