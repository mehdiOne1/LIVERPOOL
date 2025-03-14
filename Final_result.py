import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import schedule

account_sid = "AC246efe4a395db9d94a37e15d1fe145a1"
auth_token = "71a6a1a9fc494197cbc0066b1754325d"
client = Client(account_sid, auth_token)


def send_sms_message(body):
    try:
        message = client.messages.create(
            body=body,
            from_='+18782160551',  
            to='+212641153494'      
        )
        print(f"✅ رسالة مرسلة: {message.sid}")
    except Exception as e:
        print(f"❌ فشل في إرسال SMS: {e}")

def check_liverpool_match():
    url = "https://www.bbc.com/sport/football/teams/liverpool/scores-fixtures"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        matches = soup.find_all("li", class_="ssrcss-3zjzjc-HeadToHeadWrapper e1dih4s32")

        if not matches:
            print("⚠️ لم يتم العثور على مباريات. تحقق من المحدد.")
            return

        for match in matches:
    
            time_element = match.find("time", class_="ssrcss-10tlwly-StyledTime eli9aj90")
            match_time = time_element.text.strip() if time_element else "غير معروف"

       
            home_team_element = match.find("div", class_="ssrcss-bon2fo-WithInlineFallback-TeamHome e1efi6g53")
            home_team = home_team_element.find("span", {"aria-hidden": "true"}).text.strip() if home_team_element else "غير معروف"

            away_team_element = match.find("div", class_="ssrcss-nvj22c-WithInlineFallback-TeamAway e1efi6g52")
            away_team = away_team_element.find("span", {"aria-hidden": "true"}).text.strip() if away_team_element else "غير معروف"

            print(f"🆚 {home_team} vs {away_team} - 🕒 {match_time}")

            if "Liverpool" in [home_team, away_team]:
                print("🚨 مباراة ليفربول قادمة!")

   
                sms_body = f"🚨 مباراة ليفربول القادمة!\n🆚 {home_team} vs {away_team}\n🕒 {match_time}\n📺 تابع التفاصيل هنا: {url}"
                
                send_sms_message(sms_body)

    else:
        print(f"❌ فشل في جلب البيانات. كود الخطأ: {response.status_code}")


print("📡 البرنامج يعمل...")
check_liverpool_match()

