from .builder import Mode, simple_keyboard_builder

kb_start = simple_keyboard_builder(
    [
        [
            ['🧍 Профиль'],
            ['🧾 Статистика']
        ],
        [
            ['🎮 Играть']
        ]
    ],
    Mode.REPLY
)