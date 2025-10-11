from telethon import TelegramClient
import asyncio
from datetime import datetime
from config import api_id, api_hash, bot_username, alert_channel

async def check_bot():
    async with TelegramClient('session_name', api_id, api_hash) as client:
        while True:
            try:
                print(f"🕒 {datetime.now().strftime('%H:%M:%S')} - Отправляю сообщение...")
                
                await client.send_message(bot_username, '/start')
                print("Сообщение отправлено боту")
                await asyncio.sleep(10)

                responses = []
                async for message in client.iter_messages(bot_username, limit=5):
                    if message.out == False:  
                        if message.date.timestamp() > datetime.now().timestamp() - 60:
                            responses.append(message.text)
                            print(f"Бот ответил: {message.text}")
                
                if not responses:
                    print("Бот не ответил")
                    alert_message = f"""❌ВНИМАНИЕ. 
Бот отвечает с задержкой или упал. Примите меры.
Время: {datetime.now().strftime('%H:%M:%S')}
@m_savelev, @Dima_InvestProst, @daryabochkareva, @kristina_kanz
#сбой"""
                    await client.send_message(alert_channel, alert_message)
                    print("Отправлено уведомление в канал")
                else:
                    print("Бот ответил")
                
                print(f"Жду 5 минут до следующей проверки...\n")
                await asyncio.sleep(300)  
                
            except Exception as e:
                print(f"Ошибка: {e}")
                try:
                    error_message = f"Ошибка при проверке бота @{bot_username}: {str(e)}"
                    await client.send_message(alert_channel, error_message)
                    print("Отправлено уведомление об ошибке в канал")
                except:
                    print("Не удалось отправить уведомление об ошибке")
                
                print("Повтор через 5 минут...\n")
                await asyncio.sleep(300)

async def main():
    print("Запуск мониторинга бота")
    print("Уведомления будут отправляться в канал при проблемах")
    print("Для остановки нажми Ctrl+C\n")
    await check_bot()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nМониторинг остановлен")