import FoodMenu from '../components/FoodMenu';

export default function FoodPage() {
  return (
    <div>
      <div className="top-bar">
        <h1>🍔 Food & Pre-Order</h1>
        <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
          Order from your seat, skip the line
        </div>
      </div>
      <FoodMenu />
    </div>
  );
}
