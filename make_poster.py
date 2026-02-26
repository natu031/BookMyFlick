# Create all SVG posters
movies = [
    (1, 'Avengers: Endgame', '#e50914'),
    (2, 'Spider-Man', '#1e3a5f'),
    (3, 'Doctor Strange', '#4a0e4e'),
    (4, 'The Batman', '#1a1a1a'),
    (5, 'Top Gun', '#0d47a1'),
    (6, 'Jurassic World', '#2e7d32'),
    (7, 'Oppenheimer', '#3e2723'),
    (8, 'Barbie', '#f48fb1'),
    (9, 'Dune', '#ff8f00'),
    (10, 'Jawan', '#1565c0'),
    (11, 'Animal', '#b71c1c'),
    (12, 'Pathaan', '#6a1b9a'),
    (13, 'Leo', '#ff6f00'),
    (14, 'Mission Impossible', '#37474f'),
    (15, 'Fast X', '#d32f2f')
]

for id, name, color in movies:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="300" height="450">
  <rect fill="{color}" width="300" height="450"/>
  <text x="150" y="200" fill="white" font-family="Arial" font-size="20" text-anchor="middle">{name}</text>
  <text x="150" y="240" fill="white" font-family="Arial" font-size="16" text-anchor="middle">BOOKMYFLICK</text>
</svg>'''
    with open(f'static/movies/{id}.svg', 'w') as f:
        f.write(svg)
    print(f'Created {id}.svg')

print('All posters created!')
