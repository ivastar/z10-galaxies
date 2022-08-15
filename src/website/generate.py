import glob
#from .markdown_helpers import Markdown
#from .make_publication_list import Paper, main as generate_publication_list
from typing import Sequence
import os
import yaml
from yaml.loader import SafeLoader
import textwrap
import shutil
import re


def _merge_subdicts(root: dict) -> dict:
    """ Merge/flatten nested dictionaries into one. """
    res = root[0].copy()
    for sub in root[1:]:
        res.update(sub)
    return res


def get_icon(which: str) -> str:
    """ Return the icon html code for the given icon name. """
    return f"""<i class="{which:s}"></i>"""


def get_href(url: str, text: str = None, newpage:bool = True) -> str:
    """ Return the href html code for the given url. """
    if text is None:
        text = url
    if newpage:
        return f"""<a href="{url:s}" target="_blank">{text:s}</a>"""
    else:
        return f"""<a href="{url:s}">{text:s}</a>"""

class Content(dict):
    """ Parent class for all widgets. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

    @property
    def active(self):
        """ Return True if the widget is active. """
        return self['meta'].get('active', False)

    @property
    def theme_dir(self):
        """ Root directory of the theme."""
        return os.path.dirname(os.path.realpath(__file__))

    @property
    def template_dir(self):
        """ Root directory of the theme."""
        return os.path.join(self.theme_dir, 'theme')

    def build(self, **kwargs: dict):
        """ Build the section. """
        raise NotImplementedError


class Section(Content):
    """ A section of the website. """

    @property
    def template(self):
        """ Path to the index template. """
        return os.path.join(self.template_dir, 'section.html')

    def build(self, **kwargs: dict):
        """ Build the section.

        Returns
        -------
        markdown_content : str
            The content of the markdown file as a string.
        header : dict
            The header of the markdown file as a dictionary (yaml output).
        """
        # no need to bother if not active
        if self.active is False:
            print('Section {0:s} ({1:s}) is not active.'.format(self.name, self.filename))
            return '', ''
        print('Building Section {0:s} ({1:s}).'.format(self.name, self.filename))

        self.update(**kwargs)

        with open(self.template, 'r') as f:
            template = f.read()

        title = self['meta']['title']
        name = self['name']
        section_class = self.get('section_class', '')

        template = template.replace('{{name}}', name)\
                           .replace('{{other-classes}}', section_class)\
                           .replace('{{title}}', title)\
                           .replace('{{description}}', self['content'].to_html())

        # generate menu reference
        if self['meta'].get('icon', None):
            icon = get_icon(self['meta']['icon'])
        else:
            icon = ""
        ref = f"""<li><a class="nav-link scrollto" href="#{name:s}">{icon:s}<span>{title:s}</span></a></li>"""
        return template, ref


def content_from_file(filename: str,
                      **kwargs) -> "Content":
    """
    Parameters
    ----------
    filename : str
        The name of the program file to write.
    template_dir : str
        The name of the template files to use.

    Returns
    -------
    content: Content
        The content object to be used in the website.
    """
    content = Markdown.from_file(filename)
    content_type = content.meta.get('type', 'section')
    name = filename.split('/')[-1].split('.')[0]

    # add relevant categories
    type_mapping = {'section': Section,
                    'aboutme': AboutMe,
                    'contacts': Contacts,
                    'cv': CV,
                    'publications': Publications,
                    'gallery': Gallery,
                    'posts': Post}

    return type_mapping.get(content_type, Content)(
        filename = filename,
        name = name,
        content=content,
        meta=content.meta,
        type=content_type,
        **kwargs)


class Generator(dict):
    """ Main page generator. """
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    @classmethod
    def from_file(cls, path: str) -> 'Generator':
        with open(path, 'r') as f:
            return cls(**yaml.load(f, yaml.FullLoader))

    def build(self, fname: str, **kwargs):
        """ Generates the content of a markdown file.

        Parameters
        ----------
        fname : str
            The name of the markdown file to read.

        Returns
        -------
        markdown_content : str
            The content of the markdown file as a string.
        header : dict
            The header of the markdown file as a dictionary (yaml output).
        """
        content = content_from_file(fname, **kwargs)
        return content.build(**kwargs)

    @property
    def theme_dir(self):
        """ Root directory of the theme."""
        return os.path.dirname(os.path.realpath(__file__))

    @property
    def template_dir(self):
        """ Root directory of the theme."""
        return os.path.join(self.theme_dir, 'theme')

    @property
    def index_template(self):
        """ Path to the index template. """
        return os.path.join(self.template_dir, 'index.html')

    def generate(self):
        root_dir = self['sourcedir']
        build_dir = self['builddir']
        #static_dir = self['staticdir']
        #index = Markdown.from_file(os.path.join(root_dir, 'index.md'))
        #header = index.meta

        print(textwrap.dedent(f"""
        Generating website...
        ----------------------
        configuration:
            * content directory: {root_dir}
            * building directory: {build_dir}
            * theme directory: {self.theme_dir}
            * template directory: {self.template_dir}
        """))

        # construct the output folder
        if os.path.exists(build_dir):
            # remove if exists
            shutil.rmtree(build_dir)

        # copy theme resource files

        shutil.copytree(os.path.join(self.template_dir, 'assets'), os.path.join(build_dir, "assets"))
        print(os.path.join(self.template_dir, 'assets'), os.path.join(build_dir, "assets"))

        # copy static files
        #shutil.copytree(self['staticdir'],
        #                os.path.join(build_dir, "static"))

        with open(self.index_template, 'r') as f:
            print('Reading index template...', self.index_template)
            template = f.read()

        # Some global information about self
        #fname = f'{root_dir}/aboutme.md'
        #data = content_from_file(fname)

        # social links
        #social_links = []
        #for element in data['meta']['social']:
        #    icon = get_icon(element['icon'])
        #     url = element['link']
        #    social_links.append(get_href(url, text=icon, newpage=True))

        #email = [k['email'] for k in data['meta']['contact'] if 'email' in k][0]

        # background image on title
        #background_image = 'url({0:s})'.format(data['meta']['background_image'])

        # keep various sections
        #sections = []
        # Navigation bar
        #nav = []

        #for section in header['content']:
        #    fname = os.path.join(root_dir, section + '.md')
        #    txt, reference = self.build(fname,
        #                                source_dir=root_dir,
        #                                build_dir=build_dir,
        #                                baseURL=self['baseURL'],)
        #    sections.append(txt)
        #    nav.append(reference)

        table_head = generate_table_head(self['columns_title'])

        things = glob.glob('../things/*yml')
        table_body = ''
        for thing in things:
            with open(thing) as f:
                thing_yaml = yaml.load(f, Loader = SafeLoader)
                table_body += generate_table_line(thing_yaml,self['columns'])



        template = template.replace('{{table_head}}', table_head)\
                           .replace('{{table_body}}', table_body)

        # export the index.html
        with open(os.path.join(build_dir, "index.html"), 'w') as f:
            f.write(template)

        print("\nWebsite generated into {}".format(build_dir))

def generate_table_line(thing: dict = {}, columns: list = []):

    table_line = []
    table_line.append(f'<tr><th scope="row">{thing[columns[0]]["value"]}</th>')
    for col in columns[1:]:
        if col == 'default_ref':
            url = 'https://ui.adsabs.harvard.edu/abs/'+thing[col]["value"]+'/abstract'
            link = get_href(url=url, text=thing[col]["value"])
            table_line.append(f'<td>{link}</td>')
        elif col == 'default_phot_z' and thing['extra_phot_z_err_plus']['value'] and thing['extra_phot_z_err_minus']['value']:
                entry = f'{thing[col]["value"]}\
                    <span class="supsub">\
                    <sup>+{thing["extra_phot_z_err_plus"]["value"]}</sup>\
                    <sub>-{thing["extra_phot_z_err_minus"]["value"]}</sub>\
                    </span>'
                table_line.append(f'<td>{entry}</td>')

        elif col == 'extra_muv' and thing['extra_muv_err_plus']['value'] and thing['extra_muv_err_minus']['value']:
                entry = f'{thing[col]["value"]}\
                    <span class="supsub">\
                    <sup>+{thing["extra_muv_err_plus"]["value"]}</sup>\
                    <sub>-{thing["extra_muv_err_minus"]["value"]}</sub>\
                    </span>'
                table_line.append(f'<td>{entry}</td>')

        elif col == 'extra_mass' and thing['extra_mass_err_plus']['value'] and thing['extra_mass_err_minus']['value']:
                entry = f'{thing[col]["value"]}\
                    <span class="supsub">\
                    <sup>+{thing["extra_mass_err_plus"]["value"]}</sup>\
                    <sub>-{thing["extra_mass_err_minus"]["value"]}</sub>\
                    </span>'
                table_line.append(f'<td>{entry}</td>')

        elif col == 'extra_spec_z' and thing['extra_spec_z']["value"]:
            entry = f'<td>{thing[col]["value"]}'
            if thing["extra_spec_z_err"]["value"]:
                entry += f'+-{thing["extra_spec_z_err"]["value"]}</td>'
            else:
                entry += '</td>'

        else:
            table_line.append(f'<td>{thing[col]["value"]}</td>')
    table_line.append('</tr>')
    return ''.join(table_line)

def generate_table_head(columns: list = []):

    table_head = []
    table_head.append('<tr>')
    for col in columns:
        table_head.append(f'<th scope="col">{col}</th>')
    table_head.append('</tr>')
    return ''.join(table_head)

def generate_index(path: str = None):
    """ Generates the index.html file. """
    if path is None:
        path = os.path.join(os.getcwd(), 'config.yml')
    generator = Generator.from_file(path)
    generator.generate()


def generate(cfgfile: str = None):
    """ Generates the website from a given configuration file. """
    import importlib

    if cfgfile is None:
        cfgfile = os.path.join(os.getcwd(), 'config.yml')

    if not os.path.isfile(cfgfile):
        raise FileNotFoundError(f"{cfgfile} does not exist.")

    import yaml

    generator = Generator.from_file(cfgfile)
    generator.generate()
