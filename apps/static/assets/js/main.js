const apiBase = ''; // Agar backend boshqa domen yoki portda bo'lsa, shu yerga to'liq URL yozing

document.addEventListener('DOMContentLoaded', () => {
  const tbody = document.querySelector('#spot-table tbody');
  const modal = document.getElementById('modal');
  const modalTitle = document.getElementById('modal-title');
  const form = document.getElementById('spot-form');
  const addBtn = document.getElementById('add-spot-btn');
  const cancelBtn = document.getElementById('cancel-btn');

  const inputId = document.getElementById('spot-id');
  const inputZone = document.getElementById('zone');
  const inputSpotNumber = document.getElementById('spot_number');
  const selectStatus = document.getElementById('status');
  const selectSpotType = document.getElementById('spot_type');

  // Spotlar ro'yxatini yuklash
  function loadSpots() {
    fetch(apiBase + 'http://localhost:8000/api/v1/get/parking/spot')
      .then(res => res.json())
      .then(data => {
        tbody.innerHTML = '';
        data.forEach(spot => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td>${spot.id}</td>
            <td>${spot.zone}</td>
            <td>${spot.spot_number}</td>
            <td>${spot.status}</td>
            <td>${spot.spot_type}</td>
            <td>
              <button class="action-btn edit-btn" data-id="${spot.id}">Tahrirlash</button>
              <button class="action-btn delete-btn" data-id="${spot.id}">O'chirish</button>
            </td>
          `;
          tbody.appendChild(tr);
        });
        attachRowEventListeners();
      })
      .catch(err => {
        alert('Parking spotlar yuklanmadi');
        console.error(err);
      });
  }

  // Modalni ochish
  function openModal(isEdit = false, spot = null) {
    modal.classList.remove('hidden');
    if (isEdit && spot) {
      modalTitle.textContent = 'Spotni Tahrirlash';
      inputId.value = spot.id;
      inputZone.value = spot.zone;
      inputSpotNumber.value = spot.spot_number;
      selectStatus.value = spot.status;
      selectSpotType.value = spot.spot_type;
    } else {
      modalTitle.textContent = 'Yangi Spot Qo\'shish';
      form.reset();
      inputId.value = '';
    }
  }

  // Modalni yopish
  function closeModal() {
    modal.classList.add('hidden');
  }

  // Yangi spot qo'shish yoki mavjud spotni tahrirlash
  form.addEventListener('submit', e => {
    e.preventDefault();

    const spotData = {
      zone: inputZone.value.trim(),
      spot_number: inputSpotNumber.value.trim(),
      status: selectStatus.value,
      spot_type: selectSpotType.value
    };

    const id = inputId.value;

    if (id) {
      // Update
      fetch(apiBase + `http://localhost:8000/api/v1/update/parking/spot/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(spotData),
      })
        .then(res => {
          if (!res.ok) throw new Error('Spotni yangilashda xatolik yuz berdi');
          return res.json();
        })
        .then(() => {
          loadSpots();
          closeModal();
        })
        .catch(err => {
          alert(err.message);
        });
    } else {
      // Create
      fetch(apiBase + 'http://localhost:8000/api/v1/save/parking/spot/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(spotData),
      })
        .then(res => {
          if (!res.ok) throw new Error('Spot qo\'shishda xatolik yuz berdi');
          return res.json();
        })
        .then(() => {
          loadSpots();
          closeModal();
        })
        .catch(err => {
          alert(err.message);
        });
    }
  });

  // Har bir qatordagi tahrirlash va o'chirish tugmalariga event qo'shish
  function attachRowEventListeners() {
    document.querySelectorAll('.edit-btn').forEach(btn => {
      btn.onclick = () => {
        const id = btn.dataset.id;
        fetch(apiBase + `http://localhost:8000/api/v1/detail/parking/spot/${id}`)
          .then(res => res.json())
          .then(spot => {
            openModal(true, spot);
          })
          .catch(() => {
            alert('Spot ma\'lumotlari olinmadi');
          });
      };
    });

    document.querySelectorAll('.delete-btn').forEach(btn => {
      btn.onclick = () => {
        const id = btn.dataset.id;
        if (confirm('Spotni o\'chirmoqchimisiz?')) {
          fetch(apiBase + `http://localhost:8000/api/v1/delete/parking/zone/${id}`, {
            method: 'DELETE',
          })
            .then(res => {
              if (!res.ok) throw new Error('Spotni o\'chirishda xatolik yuz berdi');
              loadSpots();
            })
            .catch(err => alert(err.message));
        }
      };
    });
  }

  // Modalni bekor qilish tugmasi
  cancelBtn.addEventListener('click', () => {
    closeModal();
  });

  // Add button click
  addBtn.addEventListener('click', () => {
    openModal(false);
  });

  // Dastlabki yuklash
  loadSpots();
});
