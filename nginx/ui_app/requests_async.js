document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("teamForm");
    const teamList = document.getElementById("teamList");

    async function sendPostRequest(newMember) {
        try {
            const response = await fetch("http://localhost:8000/add-member", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(newMember)
            });
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
        }
    }

    function updateTeamList(members) {
        teamList.innerHTML = "";
        members.forEach(member => {
            const listItem = document.createElement("li");
            listItem.innerHTML = `
            <div style="display: flex; align-items: center; justify-content: space-between; width: 300px; max-width: 400px;">
                <div>
                    <strong>${member.firstName} ${member.lastName}</strong>
                    <div style="font-size: 0.8em; margin-top: 5px;">
                        ${member.role}
                    </div>
                </div>
                <button data-id="${member.id}" class="deleteBtn">🗑️</button>
            </div>
            `;
            teamList.appendChild(listItem);
        });

        document.querySelectorAll(".deleteBtn").forEach(button => {
            button.addEventListener("click", async function() {
                const memberId = this.getAttribute("data-id");
                await deleteMember(memberId);
                await fetchTeamList(); 
            });
        });
    }

    async function fetchTeamList() {
        try {
            const response = await fetch("http://localhost:8000/team");
            const teamMembers = await response.json();
            updateTeamList(teamMembers);
        } catch (error) {
            console.error('Error:', error);
        }
    }

    async function deleteMember(memberId) {
        try {
            const response = await fetch(`http://localhost:8000/member/${memberId}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                }
            });
    
            if (!response.ok) {
                const errorMessage = await response.text();
                console.error(`Error: ${response.statusText} - ${errorMessage}`);
                throw new Error(`Error: ${response.statusText}`);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
    

    form.addEventListener("submit", async function(event) {
        event.preventDefault();

        const firstName = document.getElementById("firstName").value;
        const lastName = document.getElementById("lastName").value;
        const role = document.getElementById("role").value;

        if (!firstName || !lastName || !role) {
            alert("All fields are required.");
            return;
        }

        const newMember = { firstName, lastName, role };

        await sendPostRequest(newMember);
        await fetchTeamList();
        form.reset();
    });

    fetchTeamList();
});
