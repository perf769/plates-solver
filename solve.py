from collections import deque

# ---- Конфигурация мини-игры ----
# Каждая пластина: позиция штыря 1..7, цель = 4 (центр).
# Связи направленные (одностороние): links[X] = список (Y, тип)
#   'p' = напрямую (Y двигается в ту же сторону, что X)
#   'r' = реверсивно (Y двигается в обратную сторону)
# Движение применяется только к X и его прямым целям (без каскада).

# Направление: вправо = +1 (увеличение номера отверстия), влево = -1.

def apply_move(st, links, p, d, s):
    """Сдвинуть пластину p (1..6) на s отверстий в сторону d (+1/-1)
    вместе со связанными. Вернуть новое состояние или None, если выход за край."""
    new = list(st)
    new[p - 1] += d * s
    if not (1 <= new[p - 1] <= 7):
        return None
    for (t, ty) in links[p]:
        delta = (d if ty == 'p' else -d) * s
        new[t - 1] += delta
        if not (1 <= new[t - 1] <= 7):
            return None
    return tuple(new)


def solve(links, start, goal=(4, 4, 4, 4, 4, 4)):
    """BFS по ходам игрока: один ход = пластина + сторона + кол-во отверстий.
    Минимизирует число ходов."""
    start = tuple(start)
    prev = {start: None}      # state -> (parent_state, (plate, dir, steps))
    q = deque([start])
    while q:
        st = q.popleft()
        if st == goal:
            break
        for p in range(1, 7):
            for d in (+1, -1):
                for s in range(1, 7):
                    ns = apply_move(st, links, p, d, s)
                    if ns is None:
                        break            # дальше в эту сторону тоже за край
                    if ns not in prev:
                        prev[ns] = (st, (p, d, s))
                        q.append(ns)
    if goal not in prev:
        return None
    path = []
    cur = goal
    while prev[cur] is not None:
        parent, action = prev[cur]
        path.append((action, parent))
        cur = parent
    path.reverse()
    moves = []  # (plate, dir, steps, from_pos)
    for (plate, d, s), parent in path:
        moves.append((plate, d, s, parent[plate - 1]))
    return moves


def fmt(moves):
    out = []
    for i, (plate, d, steps, frm) in enumerate(moves, 1):
        to = frm + d * steps
        side = "вправо" if d > 0 else "влево"
        out.append(f"{i}. Пластина {plate}: {frm} → {to}  ({side}, {steps} шаг."
                   f"{'' if steps == 1 else 'ов' if steps >= 5 else 'а'})")
    return "\n".join(out)


# ---- Задание 1 ----
links1 = {
    1: [(2, 'r')],
    2: [(6, 'r')],
    3: [(2, 'p'), (4, 'r'), (5, 'r'), (6, 'r')],
    4: [(3, 'r')],
    5: [(1, 'r')],
    6: [(3, 'r')],
}
start1 = (2, 2, 7, 7, 5, 3)

sol = solve(links1, start1)
if sol is None:
    print("Решение не найдено")
else:
    print(f"Решение найдено за {len(sol)} ходов:")
    print(fmt(sol))
    # --- Проверка: проигрываем ходы от старта ---
    print("\nТрассировка (позиции пластин 1..6):")
    st = tuple(start1)
    print(f"старт: {st}")
    for i, (plate, d, s, frm) in enumerate(sol, 1):
        st = apply_move(st, links1, plate, d, s)
        assert st is not None, f"Ход {i} вывел штырь за край!"
        print(f"после {i} (пласт.{plate} {'+' if d>0 else '-'}{s}): {st}")
    assert st == (4, 4, 4, 4, 4, 4), "Финал не равен цели!"
    print("\nOK: все штыри подняты (все в отверстии 4).")
