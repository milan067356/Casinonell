const tg = window.Telegram.WebApp;
tg.expand();

// Отримуємо user_id з Telegram або ставимо тестовий для перевірки
const userId = tg.initDataUnsafe?.user?.id || 123456789;

let currentMultiplier = 1.00;
let isBetted = false;
let isCashedOut = false;

async function updateState() {
    try {
        let response = await fetch(`/api/state?user_id=${userId}`);
        let data = await response.json();

        // Оновлюємо баланс
        document.getElementById('balance').innerText = data.balance.toFixed(0);

        let state = data.state;
        if (!state) return;

        let statusEl = document.getElementById('status');
        let multiplierEl = document.getElementById('multiplier');
        let actionBtn = document.getElementById('actionBtn');

        // Фаза ставок (очікування раунду)
        if (state.status === 'betting') {
            let left = Math.ceil(state.betting_left);
            statusEl.innerText = `Початок через: ${left}с`;
            multiplierEl.innerText = "1.00×";
            
            if (!isBetted) {
                actionBtn.innerText = "Поставити";
                actionBtn.disabled = false;
                actionBtn.style.background = "#0088cc";
            }
        } 
        // Фаза польоту ракети
        else if (state.status === 'flying') {
            statusEl.innerText = "Ракета летить!";
            currentMultiplier = data.current_multiplier;
            multiplierEl.innerText = currentMultiplier.toFixed(2) + "×";

            if (isBetted && !isCashedOut) {
                actionBtn.innerText = "Забрати приз";
                actionBtn.disabled = false;
                actionBtn.style.background = "#00ff88";
                actionBtn.style.color = "#000";
            }
        } 
        // Раунд завершено (краш)
        else if (state.status === 'crashed') {
            statusEl.innerText = `КРАШ на ${state.crash_point}×`;
            multiplierEl.innerText = `${state.crash_point}×`;
            multiplierEl.style.color = "#ff4444";

            if (isBetted && !isCashedOut) {
                actionBtn.innerText = "Програно";
                actionBtn.disabled = true;
            }
        }

        // Оновлення списку гравців (ваші фейкові гравці з бекенду)
        renderPlayers(state.fake_players);

    } catch (e) {
        console.error("Помилка зв'язку з сервером:", e);
    }
}

// Зміна суми ставки кнопками + / -
function changeBet(delta) {
    let input = document.getElementById('betAmount');
    let val = parseInt(input.value) + delta;
    if (val < 5) val = 5;
    input.value = val;
}

// Головна кнопка (Поставити або Забрати)
async function action() {
    let amount = parseInt(document.getElementById('betAmount').value);

    if (!isBetted) {
        // Робимо ставку
        let res = await fetch('/api/bet', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, amount: amount })
        });
        let data = await res.json();
        if (data.ok) {
            isBetted = true;
            isCashedOut = false;
            document.getElementById('actionBtn').innerText = "Очікування...";
            document.getElementById('actionBtn').disabled = true;
        } else {
            alert(data.error || "Помилка ставки");
        }
    } else if (isBetted && !isCashedOut) {
        // Забираємо виграш (кешаут)
        let res = await fetch('/api/cashout', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, multiplier: currentMultiplier })
        });
        let data = await res.json();
        if (data.ok) {
            isCashedOut = true;
            let actionBtn = document.getElementById('actionBtn');
            actionBtn.innerText = `Виграно ${data.win} ⭐`;
            actionBtn.disabled = true;
            actionBtn.style.background = "#555";
            actionBtn.style.color = "#fff";
        }
    }
}

// Рендер списку гравців унизу екрана
function renderPlayers(players) {
    let container = document.getElementById('playersList');
    container.innerHTML = players.map(p => `
        <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #222;">
            <span>${p.avatar} ${p.name}</span>
            <span style="color: #00ff88;">${p.bet} ⭐</span>
        </div>
    `).join('');
}

// Опитування сервера кожні 200 мілісекунд для плавності гри
setInterval(updateState, 200);
