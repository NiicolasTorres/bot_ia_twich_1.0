document.addEventListener("DOMContentLoaded", function() {
    const searchButton = document.getElementById("searchButton");

    searchButton.addEventListener("click", function() {
        const query = prompt("Ingresa tu consulta:");

        // Enviar la solicitud POST al bot
        fetch('/buscar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query }),
        })
        .then(response => response.json())
        .then(data => {
            // Enviar los resultados de búsqueda al chat de Twitch
            data.results.forEach(result => {
                // Reemplaza 'tuCanal' con el nombre de tu canal en Twitch
                sendChatMessage('Rolcrowley', result);
            });
        });
    });
});

// Función para enviar un mensaje al chat de Twitch
function sendChatMessage(channel, message) {
    // Reemplaza 'tuOAuthToken' con tu token de autenticación de Twitch
    const oauthToken = 'aGRGSjIxeZAVaPuZ6oOJ8pOq+oXuyVKHo4BkZoDKmxbg=';
    
    const requestOptions = {
        method: 'POST',
        headers: {
            'Client-ID': 'aub8yd14ihwn26dgr37dy144539prj', // Reemplaza 'tuClientId' con tu ID de cliente de Twitch
            'Authorization': `Bearer ${oauthToken}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            content: message,
        }),
    };

    fetch(`https://api.twitch.tv/helix/channels/chat/rulez`, requestOptions)
        .then(response => {
            if (response.ok) {
                console.log(`Mensaje enviado: ${message}`);
            } else {
                console.error('Error al enviar el mensaje al chat de Twitch');
            }
        })
        .catch(error => {
            console.error('Error al enviar el mensaje al chat de Twitch:', error);
        });
}



