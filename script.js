async function main() {
  const res = await fetch("http://127.0.0.1:5000/start", {
    method: "POST",
    headers: { "Content-Type": "application/json" }
  });

  const data = await res.json();
  const state = data.state;

  document.getElementById("dayDiv").textContent = `Day ${state.day} of 31`;
  document.getElementById("balanceDiv").textContent = `Your Balance: $${state.budget}`;
  
}

//choiceList is list of the choices (which are strings), with format "choice (cost)" 
//choiceList[0] will go in button1, etc.
async function selectChoice(buttonid, index,choiceList) {
  const res = await fetch("http://127.0.0.1:5000/submit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      choice: choice
    })
  });

  const data = await res.json();
  console.log("Updated state:", data);

  // Update UI
  document.getElementById("balance").textContent = `Your Balance: $${data.budget}`;
  document.getElementById("health").textContent = `Your Health: ${data.health}`;
  document.getElementById("day").textContent = `Day ${data.day} of 31`;

//in the display paragraph, the outcome of the choice in choiceList is displayed
document.getElementById("display").textContent = data.display[index];
document.getElementbyId(buttonid).onclick = function() {
  handleClick(newParam);
};
}


function updateOptions(data) {
  // Add the next set of options based on the game state
  for (let i = 0; i < choices.length; i++){
  document.getElementById("button1").textContent = data.options[i];
  }

  document.getElementById("display").textContent = data.display[0];
}