declare const bootstrap: {
    Modal: new (element: HTMLElement) => {
        show: () => void;
    };
};

interface Window {
    P360: P360Api;
}

type JsonObject = Record<string, unknown>;

type P360Api = {
    csrf: () => string;
    post: (url: string, data?: JsonObject) => Promise<Response>;
};

const setupConfirmationForms = (): void => {
    document.querySelectorAll<HTMLFormElement>('form[data-confirm]').forEach((form) => {
        form.addEventListener('submit', (event) => {
            if (!confirm(form.dataset.confirm ?? '')) {
                event.preventDefault();
            }
        });
    });
};

const setupLightbox = (): void => {
    const modalElement = document.getElementById('lightbox');
    if (!modalElement) {
        return;
    }

    const modal = new bootstrap.Modal(modalElement);
    document.querySelectorAll<HTMLElement>('[data-lightbox]').forEach((image) => {
        image.addEventListener('click', () => {
            const img = modalElement.querySelector('img');
            const caption = modalElement.querySelector('.caption');

            if (img) {
                img.src = image.dataset.lightbox ?? '';
            }

            if (caption) {
                caption.textContent = image.getAttribute('alt') ?? '';
            }

            modal.show();
        });
    });
};

const setupOperatorFields = (): void => {
    const roleInputs = document.querySelectorAll<HTMLInputElement>('input[name="role"]');
    const operatorFields = document.getElementById('operatorFields');

    if (!roleInputs.length || !operatorFields) {
        return;
    }

    const sync = (): void => {
        const checkedRole = document.querySelector<HTMLInputElement>('input[name="role"]:checked');
        operatorFields.classList.toggle('d-none', checkedRole?.value !== 'operator');
    };

    roleInputs.forEach((input) => input.addEventListener('change', sync));
    sync();
};

document.addEventListener('DOMContentLoaded', () => {
    setupConfirmationForms();
    setupLightbox();
    setupOperatorFields();
});

const P360: P360Api = {
    csrf: (): string => {
        const csrfMeta = document.querySelector<HTMLMetaElement>('meta[name="csrf-token"]');
        return csrfMeta ? csrfMeta.content : '';
    },
    post: (url: string, data: JsonObject = {}): Promise<Response> =>
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': P360.csrf(),
                Accept: 'application/json',
            },
            body: JSON.stringify(data),
        }),
};

window.P360 = P360;
