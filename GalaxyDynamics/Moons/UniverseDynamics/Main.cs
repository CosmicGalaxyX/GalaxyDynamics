using System;
using System.IO;
using System.Runtime.InteropServices;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Threading;


namespace UniverseDynamics
{
    public class MainWindow : Window
    {
        // =========================================================
        // RAM MONITORING
        // =========================================================

        [StructLayout(LayoutKind.Sequential)]
        public class MemoryStatus
        {
            public uint Length;
            public uint MemoryLoad;
            public ulong TotalPhysical;
            public ulong AvailablePhysical;
            public ulong TotalPageFile;
            public ulong AvailablePageFile;
            public ulong TotalVirtual;
            public ulong AvailableVirtual;
            public ulong AvailableExtendedVirtual;
        }

        [DllImport("kernel32.dll")]
        static extern bool GlobalMemoryStatusEx(MemoryStatus memoryStatus);


        // =========================================================
        // CPU MONITORING
        // =========================================================

        [StructLayout(LayoutKind.Sequential)]
        public struct SystemFileTime
        {
            public uint dwLowDateTime;
            public uint dwHighDateTime;
        }

        [DllImport("kernel32.dll")]
        static extern bool GetSystemTimes(
            out SystemFileTime idleTime,
            out SystemFileTime kernelTime,
            out SystemFileTime userTime);

        private ulong previousIdle = 0;
        private ulong previousKernel = 0;
        private ulong previousUser = 0;


        // =========================================================
        // CPU CALCULATION
        // =========================================================

        private ulong FileTimeToUInt64(SystemFileTime time)
        {
            return ((ulong)time.dwHighDateTime << 32)
                | time.dwLowDateTime;
        }

        private double GetCpuUsage()
        {
            GetSystemTimes(
                out SystemFileTime idleTime,
                out SystemFileTime kernelTime,
                out SystemFileTime userTime);

            ulong idle = FileTimeToUInt64(idleTime);
            ulong kernel = FileTimeToUInt64(kernelTime);
            ulong user = FileTimeToUInt64(userTime);

            if (previousKernel == 0)
            {
                previousIdle = idle;
                previousKernel = kernel;
                previousUser = user;

                return 0;
            }

            ulong idleDelta = idle - previousIdle;
            ulong kernelDelta = kernel - previousKernel;
            ulong userDelta = user - previousUser;

            ulong totalDelta = kernelDelta + userDelta;

            previousIdle = idle;
            previousKernel = kernel;
            previousUser = user;

            if (totalDelta == 0)
            {
                return 0;
            }

            return (1.0 - ((double)idleDelta / totalDelta)) * 100.0;
        }


        // =========================================================
        // MAIN WINDOW
        // =========================================================

        public MainWindow()
        {
            // -----------------------------------------------------
            // Window
            // -----------------------------------------------------

            Title = "Universe Dynamics";

            WindowState = WindowState.Maximized;

            Background = new SolidColorBrush(
                Color.FromRgb(5, 8, 20));


            // -----------------------------------------------------
            // Top Menu
            // -----------------------------------------------------

            Menu menu = new Menu();

            menu.Background = new SolidColorBrush(
                Color.FromRgb(11, 16, 36));


            // -----------------------------------------------------
            // RAM Text
            // -----------------------------------------------------

            TextBlock ramText = new TextBlock();

            ramText.Foreground = Brushes.White;

            ramText.FontSize = 14;

            ramText.Margin = new Thickness(10, 5, 10, 5);



            // -----------------------------------------------------
            // CPU Text
            // -----------------------------------------------------

            TextBlock cpuText = new TextBlock();

            cpuText.Foreground = Brushes.White;

            cpuText.FontSize = 14;

            cpuText.Margin = new Thickness(10, 5, 10, 5);


            // -----------------------------------------------------
            // System Update Timer
            // -----------------------------------------------------

            DispatcherTimer systemTimer = new DispatcherTimer();

            systemTimer.Interval = TimeSpan.FromSeconds(1);

            systemTimer.Tick += (sender, e) =>
            {
                // =================================================
                // RAM UPDATE
                // =================================================

                MemoryStatus memory = new MemoryStatus();

                memory.Length = (uint)Marshal.SizeOf(memory);

                GlobalMemoryStatusEx(memory);

                ulong used =
                    memory.TotalPhysical -
                    memory.AvailablePhysical;

                double usedGB =
                    used / 1024.0 / 1024.0 / 1024.0;

                double totalGB =
                    memory.TotalPhysical /
                    1024.0 / 1024.0 / 1024.0;

                ramText.Text =
                    $"RAM {memory.MemoryLoad}% • " +
                    $"{usedGB:F1} / {totalGB:F1} GB";


                // =================================================
                // CPU UPDATE
                // =================================================

                double cpuUsage = GetCpuUsage();

                cpuText.Text =
                    $"CPU {cpuUsage:F0}%";
            };

            systemTimer.Start();


            // =====================================================
            // TOP BAR
            // =====================================================

            Border topBar = new Border();

            topBar.Background = new SolidColorBrush(
                Color.FromRgb(5, 8, 36));


            StackPanel topBarContent = new StackPanel();

            topBarContent.Orientation =
                Orientation.Horizontal;


            // Add menu, RAM and CPU to the top bar
            topBarContent.Children.Add(menu);

            topBarContent.Children.Add(ramText);

            topBarContent.Children.Add(cpuText);

            // Put the content inside the top bar
            topBar.Child = topBarContent;

            // MAIN UI
        Border MainPanel = new Border();
        MainPanel.Background = new SolidColorBrush(Color.FromRgb(10,0,10));

        StackPanel MainStack = new StackPanel();
            


            // =====================================================
            // MAIN WINDOW LAYOUT
            // =====================================================

            DockPanel mainLayout = new DockPanel();


            // Put top bar at the top
            DockPanel.SetDock(
                topBar,
                Dock.Top);

            
            // Add top bar to the main layout
            mainLayout.Children.Add(topBar);
            mainLayout.Children.Add(MainPanel);

            // Set the main layout as the window content
            Content = mainLayout;

            
        }
    }


    // =============================================================
    // PROGRAM ENTRY POINT
    // =============================================================

    public class Program
    {
        [STAThread]
        public static void Main()
        {
            var app = new Application();

            var window = new MainWindow();

            app.Run(window);
        }
    }
}