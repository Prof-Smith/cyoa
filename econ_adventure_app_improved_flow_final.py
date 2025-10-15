import streamlit as st
import yaml

yaml_content = '''
chapters:
  - id: chapter_1
    title: "Supply and Demand at the Farmer's Market"
    description: "Explore basic concepts of supply and demand through a market scenario."
    start_node: start
    nodes:
      start:
        type: story
        text: "You're at a farmer's market deciding where to begin your economics journey."
        choices:
          - label: "Visit the apple stall"
            next: apple_stall
          - label: "Visit the orange stall"
            next: orange_stall

      apple_stall:
        type: story
        text: "The apple prices are high due to a recent frost. What would you like to explore?"
        choices:
          - label: "Learn about supply effects"
            next: supply_effect
          - label: "Take a quick quiz"
            next: quiz_1

      quiz_1:
        type: quiz
        question: "What happens to price when supply decreases?"
        options:
          - label: "Price increases"
            correct: true
            feedback: "Correct! Less supply usually leads to higher prices."
          - label: "Price decreases"
            correct: false
            feedback: "Not quite. Less supply tends to push prices up."
          - label: "Price stays the same"
            correct: false
            feedback: "Actually, prices usually change when supply shifts."
        next: supply_effect

      supply_effect:
        type: story
        text: "Supply changes affect price. Scarcity raises prices; abundance lowers them."
        choices:
          - label: "Attend a seminar on equilibrium"
            next: seminar
          - label: "Go home and reflect"
            next: conclusion

      seminar:
        type: story
        text: "Market equilibrium occurs where supply equals demand. Prices stabilize."
        choices:
          - label: "Finish the chapter"
            next: conclusion

      conclusion:
        type: story
        text: "You've completed your first economics adventure. Great job!"
        choices: []

  - id: chapter_2
    title: "The Role of Incentives"
    description: "Understand how incentives shape economic behavior in different contexts."
    start_node: intro
    nodes:
      intro:
        type: story
        text: "You're offered two internships: one paid, one unpaid but prestigious. What do you choose?"
        choices:
          - label: "Take the paid internship"
            next: paid_path
          - label: "Take the prestigious internship"
            next: prestige_path

      paid_path:
        type: story
        text: "You earn money but miss out on networking. What do you want to explore?"
        choices:
          - label: "Learn about monetary incentives"
            next: monetary_incentives
          - label: "Learn about opportunity cost"
            next: opportunity_cost

      prestige_path:
        type: story
        text: "You gain valuable connections but struggle financially. What do you want to explore?"
        choices:
          - label: "Learn about non-monetary incentives"
            next: non_monetary_incentives
          - label: "Learn about trade-offs"
            next: trade_offs

      monetary_incentives:
        type: story
        text: "Monetary incentives can motivate behavior, but may not always lead to optimal outcomes."
        choices:
          - label: "Finish the chapter"
            next: end

      non_monetary_incentives:
        type: story
        text: "Prestige, recognition, and experience can be powerful motivators."
        choices:
          - label: "Finish the chapter"
            next: end

      opportunity_cost:
        type: story
        text: "Opportunity cost is the value of the next best alternative you give up."
        choices:
          - label: "Finish the chapter"
            next: end

      trade_offs:
        type: story
        text: "Every decision involves trade-offs. Understanding them helps make better choices."
        choices:
          - label: "Finish the chapter"
            next: end

      end:
        type: story
        text: "You've completed the chapter on incentives. Keep thinking like an economist!"
        choices: []
'''


data = yaml.safe_load(yaml_content)
chapter_titles = {chap['title']: chap for chap in data['chapters']}
selected_title = st.selectbox("Choose a chapter:", list(chapter_titles.keys()))
chapter = chapter_titles[selected_title]
nodes = chapter['nodes']

if 'node_id' not in st.session_state or st.session_state.get('chapter_id') != chapter['id']:
    st.session_state.node_id = chapter['start_node']
    st.session_state.chapter_id = chapter['id']
    st.session_state.quiz_feedback = ""
    st.session_state.quiz_answered = False
    st.session_state.awaiting_continue = False
    st.session_state.history = []

node = nodes[st.session_state.node_id]

st.title("📚 Economics Adventure")
st.header(chapter['title'])
    
st.markdown(f"_{chapter['description']}_")

if node['type'] == 'story':
    
    st.markdown("---")
    st.markdown("### 📘 Story")
    st.markdown(node['text'])
    
    for choice in node.get('choices', []):
        if st.button(choice['label']):
            st.session_state.history.append({'node': st.session_state.node_id, 'choice': choice['label']})
            st.session_state.node_id = choice['next']
            st.session_state.quiz_feedback = ""
            st.session_state.quiz_answered = False
            st.session_state.awaiting_continue = False

elif node['type'] == 'quiz':
    
    st.markdown("---")
    st.subheader("🧠 Quiz Time")
    st.markdown("Answer the following question to test your understanding:")
    
    st.markdown(node['question'])
    if not st.session_state.quiz_answered:
        for i, option in enumerate(node['options']):
            if st.button(option['label'], key=f"opt_{i}"):
                st.session_state.quiz_feedback = option['feedback']
                st.session_state.quiz_answered = True
                st.session_state.awaiting_continue = True
                st.session_state.history.append({'node': st.session_state.node_id, 'choice': option['label'], 'feedback': option['feedback']})
    else:
        st.markdown(f"**Feedback:** {st.session_state.quiz_feedback}")

if st.session_state.awaiting_continue:
    if st.button("Continue"):
        next_node = nodes[st.session_state.node_id].get('next')
        if next_node:
            st.session_state.node_id = next_node
        st.session_state.quiz_feedback = ""
        st.session_state.quiz_answered = False
        st.session_state.awaiting_continue = False

if node['type'] == 'story' and not node.get('choices'):
    st.markdown("**[End of Chapter]**")

st.markdown("---")
st.subheader("Your Journey")
for entry in st.session_state.history:
    if 'feedback' in entry:
        st.markdown(f"**{entry['node']}** → {entry['choice']}**")
        st.markdown(f"**{entry['node']}** → {entry['choice']}  \
_Feedback_: {entry['feedback']}")
    else:
        st.markdown(f"**{entry['node']}** → {entry['choice']}**")
