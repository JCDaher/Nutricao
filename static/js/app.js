/**
 * Gerador de Dietas para Diabetes
 * Frontend JavaScript
 */

// Elementos do DOM
const form = document.getElementById('dietForm');
const submitBtn = document.getElementById('submitBtn');
const btnText = submitBtn.querySelector('.btn-text');
const btnLoading = submitBtn.querySelector('.btn-loading');
const preview = document.getElementById('preview');

// Inputs para preview
const idadeInput = document.getElementById('idade');
const pesoInput = document.getElementById('peso');
const alturaInput = document.getElementById('altura');
const sexoInputs = document.querySelectorAll('input[name="sexo"]');

// Elementos de preview
const previewImc = document.getElementById('preview-imc');
const previewClassificacao = document.getElementById('preview-classificacao');
const previewMeta = document.getElementById('preview-meta');
const previewAgua = document.getElementById('preview-agua');

/**
 * Debounce para limitar chamadas de função
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Atualiza o preview dos cálculos
 */
async function updatePreview() {
    const peso = parseFloat(pesoInput.value);
    const altura = parseFloat(alturaInput.value);
    const idade = parseInt(idadeInput.value);
    const sexo = document.querySelector('input[name="sexo"]:checked')?.value;

    // Verificar se todos os campos necessários estão preenchidos
    if (!peso || !altura || !idade || !sexo) {
        preview.classList.add('hidden');
        return;
    }

    // Validar ranges
    if (peso < 40 || peso > 300 || altura < 140 || altura > 220 || idade < 18 || idade > 100) {
        preview.classList.add('hidden');
        return;
    }

    try {
        const response = await fetch(`/api/calcular-preview?peso=${peso}&altura=${altura}&idade=${idade}&sexo=${sexo}`);

        if (!response.ok) {
            throw new Error('Erro ao calcular preview');
        }

        const data = await response.json();

        // Atualizar elementos de preview
        previewImc.textContent = `${data.imc} kg/m²`;
        previewClassificacao.textContent = data.classificacao_imc;
        previewMeta.textContent = `${data.meta_calorica} kcal`;
        previewAgua.textContent = `${data.agua_litros} L`;

        // Colorir IMC de acordo com classificação
        if (data.imc < 18.5) {
            previewImc.style.color = '#ffc107'; // Amarelo
        } else if (data.imc < 25) {
            previewImc.style.color = '#28a745'; // Verde
        } else if (data.imc < 30) {
            previewImc.style.color = '#fd7e14'; // Laranja
        } else {
            previewImc.style.color = '#dc3545'; // Vermelho
        }

        preview.classList.remove('hidden');

    } catch (error) {
        console.error('Erro no preview:', error);
        preview.classList.add('hidden');
    }
}

// Debounced version da função de preview
const debouncedUpdatePreview = debounce(updatePreview, 500);

// Event listeners para preview
[idadeInput, pesoInput, alturaInput].forEach(input => {
    input.addEventListener('input', debouncedUpdatePreview);
});

sexoInputs.forEach(input => {
    input.addEventListener('change', debouncedUpdatePreview);
});

/**
 * Define o estado de loading do botão
 */
function setLoadingState(isLoading) {
    submitBtn.disabled = isLoading;
    btnText.classList.toggle('hidden', isLoading);
    btnLoading.classList.toggle('hidden', !isLoading);
}

/**
 * Mostra mensagem de erro ao usuário
 */
function showError(message) {
    // Criar elemento de alerta
    const alert = document.createElement('div');
    alert.className = 'alert alert-error';
    alert.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        background: #fee2e2;
        border: 1px solid #fecaca;
        border-radius: 8px;
        color: #991b1b;
        font-size: 14px;
        max-width: 400px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    alert.textContent = message;

    // Adicionar animação
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);

    document.body.appendChild(alert);

    // Remover após 5 segundos
    setTimeout(() => {
        alert.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => alert.remove(), 300);
    }, 5000);
}

/**
 * Mostra mensagem de sucesso ao usuário
 */
function showSuccess(message, metadata) {
    const alert = document.createElement('div');
    alert.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        background: #d1fae5;
        border: 1px solid #a7f3d0;
        border-radius: 8px;
        color: #065f46;
        font-size: 14px;
        max-width: 400px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;

    alert.innerHTML = `
        <strong>Dieta gerada com sucesso!</strong><br>
        <small>
            IMC: ${metadata.imc} (${metadata.classificacao_imc})<br>
            Meta calórica: ${metadata.meta_calorica} kcal/dia
        </small>
    `;

    document.body.appendChild(alert);

    setTimeout(() => {
        alert.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => alert.remove(), 300);
    }, 5000);
}

/**
 * Faz o download do arquivo Markdown
 */
function downloadMarkdown(content, filename) {
    const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

/**
 * Valida o formulário antes de enviar
 */
function validateForm(formData) {
    const errors = [];

    if (!formData.nome || formData.nome.trim().length < 3) {
        errors.push('Nome deve ter pelo menos 3 caracteres');
    }

    if (!formData.sexo) {
        errors.push('Selecione o sexo');
    }

    if (!formData.idade || formData.idade < 18 || formData.idade > 100) {
        errors.push('Idade deve estar entre 18 e 100 anos');
    }

    if (!formData.peso || formData.peso < 40 || formData.peso > 300) {
        errors.push('Peso deve estar entre 40 e 300 kg');
    }

    if (!formData.altura || formData.altura < 140 || formData.altura > 220) {
        errors.push('Altura deve estar entre 140 e 220 cm');
    }

    // Validar HbA1c se preenchido
    if (formData.hba1c !== null && (formData.hba1c < 4 || formData.hba1c > 15)) {
        errors.push('HbA1c deve estar entre 4% e 15%');
    }

    // Validar glicemia se preenchida
    if (formData.glicemia !== null && (formData.glicemia < 70 || formData.glicemia > 400)) {
        errors.push('Glicemia deve estar entre 70 e 400 mg/dL');
    }

    return errors;
}

/**
 * Handler do envio do formulário
 */
async function handleSubmit(event) {
    event.preventDefault();

    // Coletar dados do formulário
    const formData = {
        nome: document.getElementById('nome').value.trim(),
        sexo: document.querySelector('input[name="sexo"]:checked')?.value || '',
        idade: parseInt(document.getElementById('idade').value) || 0,
        peso: parseFloat(document.getElementById('peso').value) || 0,
        altura: parseFloat(document.getElementById('altura').value) || 0,
        hba1c: document.getElementById('hba1c').value ? parseFloat(document.getElementById('hba1c').value) : null,
        glicemia: document.getElementById('glicemia').value ? parseFloat(document.getElementById('glicemia').value) : null
    };

    // Validar
    const errors = validateForm(formData);
    if (errors.length > 0) {
        showError(errors.join('. '));
        return;
    }

    // Ativar estado de loading
    setLoadingState(true);

    try {
        // Enviar para o backend
        const response = await fetch('/gerar-dieta', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Erro ao gerar dieta');
        }

        const data = await response.json();

        if (data.success) {
            // Download do arquivo .md
            downloadMarkdown(data.markdown, data.filename);

            // Mostrar sucesso
            showSuccess('Dieta gerada com sucesso!', data.metadata);
        } else {
            throw new Error('Resposta inválida do servidor');
        }

    } catch (error) {
        console.error('Erro:', error);
        showError(`Erro ao gerar dieta: ${error.message}`);
    } finally {
        // Desativar estado de loading
        setLoadingState(false);
    }
}

// Event listener do formulário
form.addEventListener('submit', handleSubmit);

// Prevenir submissão com Enter em campos numéricos (exceto quando está no último campo)
document.querySelectorAll('input[type="number"]').forEach(input => {
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            // Mover para o próximo campo
            const inputs = Array.from(form.querySelectorAll('input:not([type="radio"])'));
            const currentIndex = inputs.indexOf(e.target);
            if (currentIndex < inputs.length - 1) {
                inputs[currentIndex + 1].focus();
            }
        }
    });
});

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    // Focar no primeiro campo
    document.getElementById('nome').focus();

    // Verificar preview inicial se campos já estiverem preenchidos
    updatePreview();
});
