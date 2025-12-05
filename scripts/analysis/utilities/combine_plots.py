"""
SVG Plot Combiner

Combines multiple SVG files horizontally for publication figures.
Supports both command-line usage and interactive file selection.

Classes:
    SVGCombiner: Handles SVG parsing, alignment, and combination
    
Usage:
    # Command line
    python combine_plots.py file1.svg file2.svg -o combined.svg
    
    # Interactive mode
    python combine_plots.py
    
    # Programmatic usage
    combiner = SVGCombiner()
    combiner.combine_horizontal(['plot1.svg', 'plot2.svg'], 'output.svg')
"""

import os
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
import sys


class SVGCombiner:
    """
    Combines SVG files horizontally with proper alignment and spacing.
    
    Handles SVG parsing, dimension calculation, and layout arrangement
    for creating publication-ready figure panels.
    
    Attributes:
        spacing (float): Horizontal spacing between plots (default: 20)
        background_color (str): Background color for combined plot
    """
    
    def __init__(self, spacing=1, background_color='white'):
        """
        Initialize SVG combiner with layout parameters.
        
        Parameters:
        -----------
        spacing : float, optional
            Horizontal spacing between plots in pixels (default: 5)
        background_color : str, optional
            Background color for the combined SVG (default: 'white')
        """
        self.spacing = spacing
        self.background_color = background_color
    
    def parse_svg_dimensions(self, svg_path):
        """
        Extract width and height from SVG file.
        
        Parameters:
        -----------
        svg_path : str
            Path to SVG file
            
        Returns:
        --------
        tuple : (width, height) in pixels
        
        Raises:
        -------
        ValueError : If SVG dimensions cannot be parsed
        """
        try:
            tree = ET.parse(svg_path)
            root = tree.getroot()
            
            # Get dimensions from root SVG element
            width = root.get('width', '0')
            height = root.get('height', '0')
            
            # Handle different unit formats (px, pt, in, etc.)
            width = self._parse_dimension(width)
            height = self._parse_dimension(height)
            
            if width <= 0 or height <= 0:
                # Try viewBox if width/height not available
                viewbox = root.get('viewBox')
                if viewbox:
                    _, _, width, height = map(float, viewbox.split())
                else:
                    raise ValueError("Cannot determine SVG dimensions")
            
            return width, height
            
        except Exception as e:
            raise ValueError(f"Error parsing SVG {svg_path}: {str(e)}")
    
    def _parse_dimension(self, dim_str):
        """
        Parse dimension string and convert to pixels.
        
        Parameters:
        -----------
        dim_str : str
            Dimension string (e.g., '400px', '5in', '300pt')
            
        Returns:
        --------
        float : Dimension in pixels
        """
        if not dim_str:
            return 0
        
        # Remove units and convert to float
        dim_str = str(dim_str).lower()
        
        # Conversion factors to pixels
        conversions = {
            'px': 1.0,
            'pt': 1.333,  # 1 pt = 1.333 px
            'in': 96.0,   # 1 in = 96 px
            'cm': 37.8,   # 1 cm = 37.8 px
            'mm': 3.78,   # 1 mm = 3.78 px
        }
        
        for unit, factor in conversions.items():
            if dim_str.endswith(unit):
                return float(dim_str[:-len(unit)]) * factor
        
        # Assume pixels if no unit
        try:
            return float(dim_str)
        except ValueError:
            return 0
    
    def combine_horizontal(self, svg_paths, output_path, align='center'):
        """
        Combine SVG files horizontally into a single SVG.
        
        Parameters:
        -----------
        svg_paths : list of str
            Paths to input SVG files (minimum 2)
        output_path : str
            Path for output combined SVG
        align : str, optional
            Vertical alignment: 'top', 'center', 'bottom' (default: 'center')
            
        Returns:
        --------
        str : Path to created combined SVG file
        
        Raises:
        -------
        ValueError : If fewer than 2 SVG files provided
        FileNotFoundError : If input SVG files don't exist
        """
        if len(svg_paths) < 2:
            raise ValueError("At least 2 SVG files required for combination")
        
        # Validate input files
        for path in svg_paths:
            if not os.path.isfile(path):
                raise FileNotFoundError(f"SVG file not found: {path}")
        
        # Parse dimensions of all SVGs
        svg_info = []
        for path in svg_paths:
            width, height = self.parse_svg_dimensions(path)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            svg_info.append({
                'path': path,
                'width': width,
                'height': height,
                'content': content
            })
        
        # Calculate combined dimensions
        total_width = sum(info['width'] for info in svg_info) + self.spacing * (len(svg_info) - 1)
        max_height = max(info['height'] for info in svg_info)
        
        # Create combined SVG
        combined_svg = self._create_combined_svg(svg_info, total_width, max_height, align)
        
        # Write to output file
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(combined_svg)
        
        print(f"Combined SVG saved to: {output_path}")
        print(f"Final dimensions: {total_width:.0f}x{max_height:.0f} pixels")
        
        return output_path
    
    def _create_combined_svg(self, svg_info, total_width, max_height, align):
        """
        Create the combined SVG content.
        
        Parameters:
        -----------
        svg_info : list of dict
            SVG information for each file
        total_width : float
            Total width of combined SVG
        max_height : float
            Maximum height of combined SVG
        align : str
            Vertical alignment option
            
        Returns:
        --------
        str : Combined SVG content
        """
        # SVG header
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{total_width}" height="{max_height}" 
     viewBox="0 0 {total_width} {max_height}"
     xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink">
'''
        
        # Add background if specified
        if self.background_color and self.background_color.lower() != 'none':
            svg_content += f'  <rect width="100%" height="100%" fill="{self.background_color}"/>\n'
        
        # Position each SVG
        x_offset = 0
        for i, info in enumerate(svg_info):
            # Calculate vertical position based on alignment
            if align == 'top':
                y_offset = 0
            elif align == 'bottom':
                y_offset = max_height - info['height']
            else:  # center
                y_offset = (max_height - info['height']) / 2
            
            # Extract SVG content (remove xml declaration and root svg tags)
            content = self._extract_svg_content(info['content'])
            
            # Wrap in group with transform
            svg_content += f'  <g transform="translate({x_offset}, {y_offset})">\n'
            svg_content += f'    <!-- Panel {i+1}: {os.path.basename(info["path"])} -->\n'
            svg_content += content
            svg_content += '  </g>\n'
            
            # Update x offset for next SVG
            x_offset += info['width'] + self.spacing
        
        # Close SVG
        svg_content += '</svg>\n'
        
        return svg_content
    
    def _extract_svg_content(self, svg_content):
        """
        Extract inner content from SVG file (remove root svg tags).
        
        Parameters:
        -----------
        svg_content : str
            Full SVG file content
            
        Returns:
        --------
        str : Inner SVG content without root tags
        """
        try:
            # Parse the SVG
            root = ET.fromstring(svg_content)
            
            # Get all child elements as strings
            content_parts = []
            for child in root:
                content_parts.append(ET.tostring(child, encoding='unicode'))
            
            return '    ' + '\n    '.join(content_parts) + '\n'
            
        except ET.ParseError:
            # Fallback: manual extraction
            lines = svg_content.split('\n')
            start_idx = 0
            end_idx = len(lines)
            
            # Find start of content (after opening svg tag)
            for i, line in enumerate(lines):
                if '<svg' in line and '>' in line:
                    start_idx = i + 1
                    break
            
            # Find end of content (before closing svg tag)
            for i in range(len(lines) - 1, -1, -1):
                if '</svg>' in lines[i]:
                    end_idx = i
                    break
            
            content = '\n'.join(lines[start_idx:end_idx])
            return '    ' + content.replace('\n', '\n    ') + '\n'


def select_files_interactive():
    """
    Interactive file selection using tkinter dialog.
    
    Returns:
    --------
    list : Selected SVG file paths
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()  # Hide main window
        
        print("Select SVG files to combine (minimum 2)...")
        file_paths = filedialog.askopenfilenames(
            title="Select SVG files to combine",
            filetypes=[("SVG files", "*.svg"), ("All files", "*.*")]
        )
        
        root.destroy()
        
        if len(file_paths) < 2:
            print("Error: At least 2 SVG files must be selected")
            return []
        
        return list(file_paths)
        
    except ImportError:
        print("Error: tkinter not available. Please provide file paths as arguments.")
        return []


def select_output_path_interactive(input_files):
    """
    Interactive output file selection.
    
    Parameters:
    -----------
    input_files : list
        List of input file paths for default naming
        
    Returns:
    --------
    str : Output file path
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()
        
        # Generate default filename
        default_name = "combined_plots.svg"
        if input_files:
            base_dir = os.path.dirname(input_files[0])
            default_path = os.path.join(base_dir, default_name)
        else:
            default_path = default_name
        
        output_path = filedialog.asksaveasfilename(
            title="Save combined SVG as...",
            defaultextension=".svg",
            filetypes=[("SVG files", "*.svg"), ("All files", "*.*")],
            initialfile=default_name
        )
        
        root.destroy()
        
        return output_path or default_path
        
    except ImportError:
        return "combined_plots.svg"


def main():
    """
    Main function for command-line interface.
    """
    parser = argparse.ArgumentParser(
        description="Combine SVG files horizontally for publication figures",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python combine_plots.py plot1.svg plot2.svg -o combined.svg
  python combine_plots.py *.svg --spacing 30 --align top
  python combine_plots.py  # Interactive mode
        """
    )
    
    parser.add_argument(
        'files', 
        nargs='*', 
        help='SVG files to combine (minimum 2). If none provided, opens file dialog.'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output SVG file path (default: combined_plots.svg)'
    )
    
    parser.add_argument(
        '-s', '--spacing',
        type=float,
        default=5,
        help='Horizontal spacing between plots in pixels (default: 5)'
    )
    
    parser.add_argument(
        '-a', '--align',
        choices=['top', 'center', 'bottom'],
        default='center',
        help='Vertical alignment of plots (default: center)'
    )
    
    parser.add_argument(
        '-b', '--background',
        default='white',
        help='Background color (default: white, use "none" for transparent)'
    )
    
    args = parser.parse_args()
    
    # Get input files
    if args.files:
        input_files = args.files
        if len(input_files) < 2:
            print("Error: At least 2 SVG files required")
            sys.exit(1)
    else:
        print("No files provided. Opening file selection dialog...")
        input_files = select_files_interactive()
        if not input_files:
            print("No files selected. Exiting.")
            sys.exit(1)
    
    # Get output path
    if args.output:
        output_path = args.output
    else:
        if not args.files:  # Interactive mode
            output_path = select_output_path_interactive(input_files)
        else:
            output_path = "combined_plots.svg"
    
    # Validate input files
    for file_path in input_files:
        if not os.path.isfile(file_path):
            print(f"Error: File not found: {file_path}")
            sys.exit(1)
        if not file_path.lower().endswith('.svg'):
            print(f"Warning: {file_path} may not be an SVG file")
    
    # Create combiner and combine files
    try:
        combiner = SVGCombiner(
            spacing=args.spacing,
            background_color=args.background
        )
        
        print(f"Combining {len(input_files)} SVG files...")
        for i, file_path in enumerate(input_files, 1):
            print(f"  {i}. {os.path.basename(file_path)}")
        
        result_path = combiner.combine_horizontal(
            input_files, 
            output_path, 
            align=args.align
        )
        
        print(f"\n✓ Successfully combined SVG files!")
        print(f"Output: {os.path.abspath(result_path)}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()