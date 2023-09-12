from setuptools import setup, find_packages

requires = [
    'flash',
    'spotipy',
    'html5lib',
    'pathlib',
    'pandas',
]

setup(
    name='SpotifyMusicJournal',
    version='1.0',
    description='Spotify Music Journal API to create journal entries based on music',
    author='Gwyneth Chiu',
    author_email='gwynethwongchiu@gmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)
