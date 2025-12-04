!pip3 install lucide-react
import '../styles/globals.css';
import { useState, useEffect } from 'react';
import { BuildingCard } from './components/BuildingCard';
import { Dumbbell, UtensilsCrossed, BookOpen, Coffee, Wifi, RefreshCw } from 'lucide-react';
import { Button } from './components/ui/button';

// Mock data generator
const generateHourlyData = (baseOccupancy: number) => {
  const hours = ['8am', '9am', '10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm'];
  return hours.map((hour, index) => ({
    hour,
    occupancy: Math.max(0, Math.min(100, baseOccupancy + (Math.random() - 0.5) * 30 - index * 2))
  }));
};

export default function App() {
  const [lastUpdate, setLastUpdate] = useState(new Date());
  const [buildings, setBuildings] = useState([
    {
      name: 'PAC (Gym)',
      type: 'Recreation',
      currentOccupancy: 245,
      capacity: 350,
      trend: 'up' as const,
      hourlyData: generateHourlyData(70),
      icon: <Dumbbell className="w-6 h-6 text-blue-400" />
    },
    {
      name: 'Daniel Dining Hall',
      type: 'Food Services',
      currentOccupancy: 156,
      capacity: 400,
      trend: 'stable' as const,
      hourlyData: generateHourlyData(39),
      icon: <UtensilsCrossed className="w-6 h-6 text-purple-400" />
    },
    {
      name: 'Library',
      type: 'Study Space',
      currentOccupancy: 412,
      capacity: 600,
      trend: 'up' as const,
      hourlyData: generateHourlyData(69),
      icon: <BookOpen className="w-6 h-6 text-pink-400" />
    },
    {
      name: 'Trone Student Center',
      type: 'Common Area',
      currentOccupancy: 89,
      capacity: 250,
      trend: 'down' as const,
      hourlyData: generateHourlyData(36),
      icon: <Coffee className="w-6 h-6 text-emerald-400" />
    }
    
  ]);

  const refreshData = () => {
    setBuildings(prev => prev.map(building => ({
      ...building,
      currentOccupancy: Math.max(0, Math.min(building.capacity, 
        building.currentOccupancy + Math.floor((Math.random() - 0.5) * 20)
      )),
      hourlyData: generateHourlyData((building.currentOccupancy / building.capacity) * 100)
    })));
    setLastUpdate(new Date());
  };

  // Auto refresh every 30 seconds
  useEffect(() => {
    const interval = setInterval(refreshData, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 relative overflow-hidden">
      {/* Animated background effects */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-0 -left-4 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob" />
        <div className="absolute top-0 -right-4 w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000" />
        <div className="absolute -bottom-8 left-20 w-96 h-96 bg-pink-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000" />
      </div>

      {/* Main Content */}
      <div className="relative z-10">
        {/* Header */}
        <div className="border-b border-white/10 bg-black/20 backdrop-blur-xl">
          <div className="max-w-7xl mx-auto px-6 py-8">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-white mb-2">Furman University Campus Activity Monitor</h1>
                <p className="text-white/60">
                  Real-time occupancy data across campus buildings
                </p>
              </div>
              <Button 
                onClick={refreshData}
                className="bg-white/10 hover:bg-white/20 border border-white/20 text-white backdrop-blur-sm"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                Refresh
              </Button>
            </div>
            
            {/* Stats Overview */}
            <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-4">
                <div className="text-white/60 text-sm mb-1">Total Occupancy</div>
                <div className="text-white text-2xl">
                  {buildings.reduce((sum, b) => sum + b.currentOccupancy, 0)}
                </div>
              </div>
              <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-4">
                <div className="text-white/60 text-sm mb-1">Average Capacity</div>
                <div className="text-white text-2xl">
                  {Math.round(buildings.reduce((sum, b) => sum + (b.currentOccupancy / b.capacity * 100), 0) / buildings.length)}%
                </div>
              </div>
              <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-4">
                <div className="text-white/60 text-sm mb-1">Last Updated</div>
                <div className="text-white text-2xl">
                  {lastUpdate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Building Grid */}
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {buildings.map((building) => (
              <BuildingCard key={building.name} building={building} />
            ))}
          </div>

          {/* Info Footer */}
          <div className="mt-12 text-center">
            <div className="inline-block bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl px-6 py-3">
              <p className="text-white/60 text-sm">
                Data updates automatically every 30 seconds • Connect your data source to see real-time campus activity
              </p>
            </div>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes blob {
          0%, 100% {
            transform: translate(0, 0) scale(1);
          }
          25% {
            transform: translate(20px, -50px) scale(1.1);
          }
          50% {
            transform: translate(-20px, 20px) scale(0.9);
          }
          75% {
            transform: translate(50px, 50px) scale(1.05);
          }
        }

        .animate-blob {
          animation: blob 7s infinite;
        }

        .animation-delay-2000 {
          animation-delay: 2s;
        }

        .animation-delay-4000 {
          animation-delay: 4s;
        }
      `}</style>
    </div>
  );
}
