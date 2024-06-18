// Espera até que o DOM esteja completamente carregado
document.addEventListener("DOMContentLoaded", function() {
    // Obtém elementos do DOM necessários
    const menuToggle = document.getElementById("menu-toggle");
    const menu = document.getElementById("menu");
    const h2Elements = document.querySelectorAll(".options h2");

    // Adiciona um ouvinte de evento para o clique no botão de menu
    menuToggle.addEventListener("click", toggleMenu);

    // Adiciona ouvintes de evento para os cabeçalhos das opções
    h2Elements.forEach(function(h2) {
        h2.addEventListener("click", toggleOptions);
    });

    // Atualiza o rodapé
    updateFooter();
});

// Função para alternar o menu
function toggleMenu() {
    menu.classList.toggle("collapsed");
}

// Função para alternar as opções
function toggleOptions() {
    // Obtém o próximo elemento "ul" após o cabeçalho clicado
    const nextUl = this.nextElementSibling;
    // Obtém o ícone de chevron dentro do cabeçalho clicado
    const chevronIcon = this.querySelector(".fas.fa-chevron-down");

    // Se o próximo ul estiver visível, esconde-o e reajusta o ícone
    if (nextUl.style.display === "block") {
        nextUl.style.display = "none";
        chevronIcon.style.transform = "";
        chevronIcon.style.top = "";
    } else { // Caso contrário, mostra-o e ajusta o ícone
        nextUl.style.display = "block";
        chevronIcon.style.transform = "rotate(-90deg)";
        chevronIcon.style.top = "10px";
    }
}


