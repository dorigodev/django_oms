// __tests__/orderModal.test.js
const { openModal, closeModal } = require('../orderModal');  // ajuste o caminho se necessário

test('Deve abrir o modal quando a função openModal for chamada', () => {
  document.body.innerHTML = `<div id="statusModal" style="display: none;"></div>`;  // mock do HTML
  openModal(1);
  const modal = document.getElementById('statusModal');
  expect(modal.style.display).toBe("block");
});

test('Deve fechar o modal quando a função closeModal for chamada', () => {
  document.body.innerHTML = `<div id="statusModal" style="display: block;"></div>`;  // mock do HTML
  closeModal();
  const modal = document.getElementById('statusModal');
  expect(modal.style.display).toBe("none");
});
