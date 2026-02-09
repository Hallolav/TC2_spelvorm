import streamlit as st
import random
import time
import base64

# Functies uit de notebook
def willekeurig_traject(aantal_schaatsers, type_wedstrijd, type_trein):
    if type_trein == "intercity":
        aantal_rondjes = random.randint(4, 8)
    elif type_trein == "sprinter":
        aantal_rondjes = random.randint(2, 5)
    else:
        raise ValueError("Ongeldig type trein. Kies 'intercity' of 'sprinter'.")

    traject_dict = {
        "Maastricht -> Den Helder": 8,
        "Vlissingen -> Groningen": 8,          
        "Groningen -> Rotterdam": 8,           
        "Maastricht -> Haarlem": 8,       
        "Alkmaar -> Maastricht": 7,
        "Enschede -> Den Haag": 7,             
        "Leeuwarden -> Rotterdam": 7,          
        "Heerlen -> Alkmaar": 7,     
        "Heerlen -> Den Helder": 6,
        "Nijmegen -> Den Helder": 6,
        "Leeuwarden -> Den Haag": 6,           
        "Enschede -> Schiphol": 6,  
        "Enschede -> Schiphol": 5,
        "Den Haag -> Schiphol": 5,
        "Roosendaal -> Zwolle": 5,
        "Maastricht -> Utrecht": 5,   
        "Eindhoven -> Schiphol": 4,            
        "Zwolle -> Groningen": 4,              
        "Rotterdam -> Breda": 4,    
        "Utrecht -> Arnhem": 4,     
        "Amsterdam -> Schiphol": 3,            
        "Rotterdam -> Den Haag": 3,            
        "Utrecht -> Amersfoort": 3, 
        "Zwolle -> Meppel": 3,      
        "Leiden -> Den Haag": 2,    
        "Rotterdam -> Schiedam": 2, 
        "Amsterdam -> Haarlem": 2,  
        "Eindhoven -> Helmond": 2   
    }

    # Kies een traject met lengte 5 (dit lijkt een bug in originele code, maar ik behoud het)
    traject = random.choice([k for k, v in traject_dict.items() if v == 5])

    if type_wedstrijd == "langebaan":
        aantal_rondjes = aantal_rondjes
    elif type_wedstrijd == "shorttrack":
        aantal_rondjes = aantal_rondjes * 3
    else:
        raise ValueError("Ongeldig type wedstrijd. Kies 'langebaan' of 'shorttrack'.")

    return aantal_rondjes, traject

def willekeurige_opdrachten(aantal_schaatsers):
    opdrachten = [None] * aantal_schaatsers

    # deel als eerste de opdracht machinist uit
    aantal_machinisten = random.randint(1, aantal_schaatsers//3)
    machinisten = random.sample(range(aantal_schaatsers), aantal_machinisten)
    for i in machinisten:
        opdrachten[i] = "machinist"

    # verdeel daarna stoelnummers
    aantal_stoelen = (aantal_schaatsers - aantal_machinisten) // 2
    if random.choice([True, True, False]):
        # oneven stoelen
        stoelnummers = [x * 2 + 1 for x in range(aantal_stoelen)]
    else:
        # even stoelen
        stoelnummers = [x * 2 for x in range(1, aantal_stoelen)]

    for opdrachtnummer in range(aantal_schaatsers):
        if opdrachten[opdrachtnummer] is None:
            opdrachten[opdrachtnummer] = random.choice(stoelnummers)

    return opdrachten

def show_boarding_pass(aantal_rondjes, traject):
    current_date = time.strftime("%d-%m-%Y")
    with open("NS-logo.png", "rb") as f:
        img_data = base64.b64encode(f.read()).decode()
    html_table = f"""
    <table border="1" style="width:100%; border-collapse: collapse;">
        <tr>
            <td rowspan="5" colspan="2" style="text-align: center; vertical-align: middle;">
                <img src="data:image/png;base64,{img_data}" alt="NS Logo" style="width:100px;">
            </td>
            <td colspan="2" style="text-align: center; font-weight: bold;">NS-treinticket</td>
        </tr>
        <tr>
            <td>Geldig op: {current_date}</td>
            <td></td>
        </tr>
        <tr>
            <td>{traject} (enkele reis)</td>
            <td></td>
        </tr>
        <tr>
            <td>Lengte traject: <b>{aantal_rondjes} rondjes</b></td>
            <td>Tweede klasse</td>
        </tr>
        <tr>
            <td></td>
            <td>Prijs: 0 euro</td>
        </tr>
    </table>
    """
    return html_table

# Streamlit app
def main():
    if 'state' not in st.session_state:
        st.session_state.state = 'input'
        st.session_state.aantal_schaatsers = 7
        st.session_state.type_wedstrijd = 'langebaan'
        st.session_state.type_trein = 'intercity'
        st.session_state.traject = None
        st.session_state.aantal_rondjes = None
        st.session_state.opdrachten = None
        st.session_state.current_opdracht = 0

    if st.session_state.state == 'input':
        col1, col2 = st.columns(2)
        with col1:
            st.image("NS-logo.png")
        with col2:
            st.image("Tjaslogo.png")
        st.title("NS-spel schaatstraining")
        st.header("Speluitleg")
        st.write("""
Het NS-spel is geïnspireerd op de treinen van de NS. Het is bedoeld om aan conditie te werken op een speelse manier. Daarnaast leren rijders het marathonspelletje te spelen: hoe stap je tussen een rijdende trein, hoe kun je de eindsprint het beste timen, hoe kun je het best iemand inhalen? 

Deze training is geschikt voor schaatsers in het niveau “train trainen” en “trainen om te presteren” uit het MJOP. Er is een competitieve component in deze training die schaatsers motiveert hun best te doen. Echter, de wedstrijd is in zo’n manier opgebouwd dat niet de sterkste schaatser per se wint. Het belangrijkste onderdeel in deze training is leren om het marathonspel te leren spelen. Tussendoor evalueren de rijders samen hoe het gegaan is, en delen tips en tops uit aan elkaar. Op deze manier leren rijders van elkaar (regie overdragen). 

Dit spel (en de bijbehorende website) is geschreven door Olav. Van Tjas, weetjewel. Vind je dit nou leuk? Stuur eens een berichtje!
             """)
        st.header("Parameters invoeren")

        aantal_schaatsers = st.number_input("Aantal schaatsers", min_value=1, max_value=20, value=7, step=1)
        type_wedstrijd = st.radio("Type wedstrijd", ["langebaan", "shorttrack"])
        type_trein = st.radio("Type trein", ["intercity", "sprinter"])

        if st.button("Bevestig"):
            if aantal_schaatsers < 5 or aantal_schaatsers > 10:
                st.error("Het aantal schaatsers moet tussen 5 en 10 zijn.")
            else:
                st.session_state.aantal_schaatsers = aantal_schaatsers
                st.session_state.type_wedstrijd = type_wedstrijd
                st.session_state.type_trein = type_trein
                st.session_state.aantal_rondjes, st.session_state.traject = willekeurig_traject(aantal_schaatsers, type_wedstrijd, type_trein)
                st.session_state.opdrachten = willekeurige_opdrachten(aantal_schaatsers)
                st.session_state.current_opdracht = 0
                st.session_state.state = 'show_traject'
                st.rerun()

    elif st.session_state.state == 'show_traject':
        html_table = show_boarding_pass(st.session_state.aantal_rondjes, st.session_state.traject)
        st.markdown(html_table, unsafe_allow_html=True)

        if st.session_state.current_opdracht < st.session_state.aantal_schaatsers:
            if st.button(f"Toon opdracht voor persoon {st.session_state.current_opdracht + 1}"):
                st.session_state.state = 'show_opdracht'
                st.rerun()
        else:
            st.session_state.state = 'input'
            st.rerun()

    elif st.session_state.state == 'show_opdracht':
        html_table = show_boarding_pass(st.session_state.aantal_rondjes, st.session_state.traject)
        st.markdown(html_table, unsafe_allow_html=True)

        opdracht_placeholder = st.empty()
        if st.session_state.opdrachten[st.session_state.current_opdracht] == "machinist":
            opdracht = "machinist"
        else:
            opdracht = f"stoelnummer {st.session_state.opdrachten[st.session_state.current_opdracht]}"  
        opdracht_placeholder.header(f"jouw opdracht is: {opdracht}")

        progress_placeholder = st.empty()
        wachttijd = 5
        for i in range(wachttijd, 0, -1):
            progress_placeholder.progress(i / wachttijd)
            time.sleep(1)
        progress_placeholder.empty()
        opdracht_placeholder.empty()

        st.session_state.current_opdracht += 1
        if st.session_state.current_opdracht < st.session_state.aantal_schaatsers:
            st.session_state.state = 'show_traject'
        else:
            st.session_state.state = 'input'
        st.rerun()

if __name__ == "__main__":
    main()