from random import choice
from engine.team_generator import TeamGenerator
from engine.match_context import MatchContext
from engine.match_engine import MatchEngine

# === 1. Генерация команд ===
generator = TeamGenerator()
team_a = generator.generate_team("Team A")
team_b = generator.generate_team("Team B")

# === 2. Инициализация контекста (внутри создаётся мяч, аналитика и трекер)
context = MatchContext(team_a=team_a, team_b=team_b)

# === 3. Назначим начальные зоны для всех игроков
for player in context.all_players:
    context.zone_tracker.update_player_zone(
        player,
        choice(context.zone_analyzer.zones)  # случайная зона из доступных
    )

# === 4. Симуляция матча
engine = MatchEngine(context=context, zone_tracker=context.zone_tracker)

from visualization import Visualizer

visualizer = Visualizer(context, engine)
visualizer.run(ticks=10)