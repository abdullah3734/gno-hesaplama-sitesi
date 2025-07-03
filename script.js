function bilesenEkle(dersIndex) {
    const container = document.getElementById(`bilesenler-container-${dersIndex}`);
    
    const yeniBilesen = document.createElement('div');
    yeniBilesen.classList.add('bilesen-satiri');
    
    yeniBilesen.innerHTML = `
        <input type="text" name="ders-${dersIndex}-bilesen-ad" placeholder="Bileşen Adı" required>
        <input type="number" name="ders-${dersIndex}-bilesen-not" placeholder="Not" min="0" max="100" required>
        <input type="number" name="ders-${dersIndex}-bilesen-yuzde" placeholder="Yüzde (%)" min="0" max="100" required>
        <button type="button" class="sil-btn" onclick="this.parentElement.remove()">Sil</button>
    `;
    
    container.appendChild(yeniBilesen);
}