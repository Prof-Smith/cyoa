
import streamlit as st
import yaml

# YAML content for the adventure
yaml_content = """
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
"""

# Load YAML content
data = yaml.safe_load(yaml_content)
chapter = data['chapters'][0]
nodes = chapter['nodes']

# Initialize session state
if 'node_id' not in st.session_state:
    st.session_state.node_id = chapter['start_node']
if 'quiz_feedback' not in st.session_state:
    st.session_state.quiz_feedback = ""
if 'show_continue' not in st.session_state:
    st.session_state.show_continue = False

node = nodes[st.session_state.node_id]
st.title(chapter['title'])
st.markdown(f"_{chapter['description']}_")

if node['type'] == 'story':
    st.markdown(node['text'])
    for choice in node['choices']:
        if st.button(choice['label']):
            st.session_state.node_id = choice['next']
            st.session_state.quiz_feedback = ""
            st.session_state.show_continue = False
            st.experimental_rerun()

elif node['type'] == 'quiz':
    st.subheader("Quiz")
    st.markdown(node['question'])
    for option in node['options']:
        if st.button(option['label']):
            st.session_state.quiz_feedback = option['feedback']
            st.session_state.node_id = node['next']
            st.session_state.show_continue = True
            st.experimental_rerun()

if st.session_state.quiz_feedback:
    st.markdown(f"**Feedback:** {st.session_state.quiz_feedback}")

if st.session_state.show_continue:
    if st.button("Continue"):
        st.session_state.quiz_feedback = ""
        st.session_state.show_continue = False
        st.experimental_rerun()

if not node['choices']:
    st.markdown("**[End of Chapter]**")
