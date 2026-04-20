import { useState } from 'react';

const MENU = [
  { id: 'f1', name: 'Vada Pav', price: 60, category: 'Snacks', prep: 2, veg: true },
  { id: 'f2', name: 'Chicken Tikka Roll', price: 180, category: 'Main', prep: 5, veg: false },
  { id: 'f3', name: 'Paneer Tikka Roll', price: 160, category: 'Main', prep: 5, veg: true },
  { id: 'f4', name: 'Masala Dosa', price: 120, category: 'Main', prep: 7, veg: true },
  { id: 'f5', name: 'Pav Bhaji', price: 100, category: 'Snacks', prep: 4, veg: true },
  { id: 'f6', name: 'Samosa (2 pcs)', price: 50, category: 'Snacks', prep: 2, veg: true },
  { id: 'f7', name: 'Cold Coffee', price: 120, category: 'Beverages', prep: 3, veg: true },
  { id: 'f8', name: 'Fresh Lime Soda', price: 80, category: 'Beverages', prep: 2, veg: true },
  { id: 'f9', name: 'Mango Lassi', price: 100, category: 'Beverages', prep: 3, veg: true },
  { id: 'f10', name: 'French Fries', price: 90, category: 'Snacks', prep: 4, veg: true },
  { id: 'f11', name: 'Chicken Biryani', price: 220, category: 'Main', prep: 8, veg: false },
  { id: 'f12', name: 'Pepsi 500ml', price: 60, category: 'Beverages', prep: 1, veg: true },
  { id: 'f13', name: 'Ice Cream Sundae', price: 140, category: 'Desserts', prep: 3, veg: true },
  { id: 'f14', name: 'Nachos with Cheese', price: 150, category: 'Snacks', prep: 4, veg: true },
  { id: 'f15', name: 'Butter Chicken Meal', price: 250, category: 'Main', prep: 10, veg: false },
];

const CATEGORIES = ['All', 'Snacks', 'Main', 'Beverages', 'Desserts'];

export default function FoodMenu() {
  const [filter, setFilter] = useState('All');
  const [orders, setOrders] = useState([]);

  const filtered = filter === 'All' ? MENU : MENU.filter((f) => f.category === filter);

  const addOrder = (item) => {
    setOrders((prev) => [...prev, { ...item, orderedAt: new Date().toLocaleTimeString() }]);
  };

  return (
    <div>
      <div style={{ display: 'flex', gap: '8px', marginBottom: '20px', flexWrap: 'wrap' }}>
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            className="suggestion-chip"
            style={filter === cat ? { background: 'rgba(59,130,246,0.2)', color: 'var(--accent-blue)', borderColor: 'rgba(59,130,246,0.4)' } : {}}
            onClick={() => setFilter(cat)}
          >
            {cat}
          </button>
        ))}
      </div>

      {orders.length > 0 && (
        <div className="glass-card" style={{ padding: '16px', marginBottom: '20px', borderLeft: '3px solid var(--accent-green)' }}>
          <div style={{ fontSize: '0.85rem', fontWeight: 700, marginBottom: '8px', color: 'var(--accent-green)' }}>
            🛒 Your Orders ({orders.length})
          </div>
          {orders.map((o, i) => (
            <div key={i} style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', padding: '4px 0' }}>
              {o.name} — ₹{o.price} • Ordered at {o.orderedAt} • Ready in ~{o.prep} min
            </div>
          ))}
          <div style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--accent-cyan)', marginTop: '8px' }}>
            Total: ₹{orders.reduce((sum, o) => sum + o.price, 0)}
          </div>
        </div>
      )}

      <div className="food-grid">
        {filtered.map((item) => (
          <div key={item.id} className="glass-card food-card">
            <div className="food-name">
              <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span className={`veg-badge ${item.veg ? 'veg' : 'non-veg'}`} />
                {item.name}
              </span>
            </div>
            <div className="food-meta">
              <span>{item.category}</span>
              <span>⏱ {item.prep} min prep</span>
            </div>
            <div className="food-price">₹{item.price}</div>
            <button className="food-order-btn" onClick={() => addOrder(item)}>
              Pre-Order — Skip the Line
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
