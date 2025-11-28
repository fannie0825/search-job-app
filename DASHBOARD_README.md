# CareerLens Dashboard Components

Complete dashboard implementation for CareerLens with responsive design and dark mode support.

## Components Overview

### 1. **DashboardLayout** (`components/DashboardLayout.jsx`)
Main layout component that orchestrates the entire dashboard view.

**Features:**
- Responsive layout with sidebar and main content
- Mobile hamburger menu
- Dark mode support
- Scrollable main content area

**Usage:**
```jsx
import DashboardLayout from './components/DashboardLayout';

function App() {
  return <DashboardLayout />;
}
```

### 2. **Sidebar** (`components/Sidebar.jsx`)
Fixed left sidebar with filters and controls.

**Features:**
- CareerLens logo header
- Resume upload drop zone (PDF/DOCX)
- Target Industries input with tags
- Salary range slider (HK$4k - HK$90k)
- "Analyze & Benchmark" primary action button
- Responsive: transforms to drawer on mobile

**Props:**
- `isOpen` (boolean): Controls sidebar visibility on mobile
- `onClose` (function): Callback to close sidebar
- `isMobile` (boolean): Indicates mobile viewport

### 3. **MarketPositionCards** (`components/MarketPositionCards.jsx`)
Three-card grid displaying market positioning metrics.

**Cards:**
1. **Estimated Salary Band**: HK$45k-60k with success indicator
2. **Top Skill Gap**: Cloud Architecture with warning indicator
3. **Recommended Accreditation**: AWS Certified Solutions Architect

**Features:**
- Icon-based visual indicators
- Color-coded status (success/warning/info)
- Delta indicators showing market comparison
- Dark mode compatible

### 4. **JobMatchTable** (`components/JobMatchTable.jsx`)
Interactive table displaying ranked job matches.

**Features:**
- Expandable rows with accordion logic
- Match score progress bars (color-coded)
- "Tailor Resume" action buttons
- Detailed fit analysis on expansion
- Missing skill identification

**Table Columns:**
- Rank
- Job Title
- Company
- Location (HK)
- Match Score (visual progress bar + percentage)
- Fit Type
- Action (Tailor Resume button)

**Interactive Features:**
- Click row to expand/collapse
- Expanded rows show:
  - "Why this fits" explanation
  - "Missing skill" identification
  - Link to full job description

## Styling & Design System

All components use the CareerLens design system defined in `tailwind.config.js` and `globals.css`:

- **Colors**: Navy sidebar, Accent Blue for actions, Status colors for indicators
- **Typography**: Inter font family
- **Dark Mode**: Class-based dark mode support
- **Responsive**: Mobile-first design with breakpoints

## Responsive Behavior

### Desktop (≥1024px)
- Fixed sidebar on left (256px width)
- Main content area scrollable
- Full table view

### Mobile (<1024px)
- Hamburger menu in header
- Sidebar becomes overlay drawer
- Table becomes horizontally scrollable
- Cards stack vertically

## Dark Mode

Dark mode is implemented using Tailwind's class-based strategy:

```jsx
// Toggle dark mode
document.documentElement.classList.toggle('dark');
```

All components automatically adapt colors:
- Sidebar: Dark navy background
- Cards: Dark gray backgrounds
- Text: White/light gray
- Borders: Adjusted for contrast

## Interactive Features

### Resume Upload
- File input accepts PDF and DOCX
- Visual drop zone with hover effects
- Console logs uploaded file name

### Salary Slider
- Range: HK$4k to HK$90k
- Visual progress indicator
- Real-time value display

### Industry Tags
- Type and press Enter to add
- Click X to remove
- Visual tag chips

### Job Match Table
- Click row to expand details
- "Tailor Resume" button triggers console log
- Expandable accordion sections

## Mock Data

The dashboard uses mock data for demonstration:

- **5 job matches** with varying match scores (75-92%)
- **Market positioning** metrics
- **Skill gaps** and recommendations

Replace with real API calls in production.

## Installation & Setup

1. **Install dependencies:**
```bash
npm install
```

2. **Required packages:**
- `react` & `react-dom`
- `lucide-react` (for icons)
- `tailwindcss` (for styling)

3. **Import styles:**
```jsx
import './globals.css';
```

4. **Use components:**
```jsx
import DashboardLayout from './components/DashboardLayout';

function App() {
  return <DashboardLayout />;
}
```

## File Structure

```
/workspace
├── components/
│   ├── DashboardLayout.jsx    # Main layout orchestrator
│   ├── Sidebar.jsx             # Left sidebar with filters
│   ├── MarketPositionCards.jsx # 3-card grid for metrics
│   ├── JobMatchTable.jsx       # Interactive job matches table
│   └── Logo.jsx                # CareerLens logo component
├── globals.css                 # Tailwind styles & design system
├── tailwind.config.js          # Tailwind configuration
└── App.jsx                     # Root application component
```

## Customization

### Update Mock Data
Edit the `mockJobs` array in `JobMatchTable.jsx` and the `cards` array in `MarketPositionCards.jsx`.

### Change Colors
Update color values in `tailwind.config.js` and `globals.css`.

### Modify Layout
Adjust spacing, sizing, and breakpoints in component files using Tailwind classes.

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile)
- Requires CSS Grid and Flexbox support

## Accessibility

- Semantic HTML elements
- ARIA labels on interactive elements
- Keyboard navigation support
- Focus visible states
- Screen reader friendly

## Next Steps

1. Connect to real API endpoints
2. Implement actual file upload functionality
3. Add loading states and error handling
4. Implement toast notifications for actions
5. Add data persistence (localStorage/API)
6. Add filtering and sorting functionality
7. Implement actual resume tailoring logic
