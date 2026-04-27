---
title: "Mvvm"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [architecture, software-design, ui-patterns, xamarin, wpf]
---

# MVVM (Model-View-ViewModel)

## Overview

MVVM, or Model-View-ViewModel, is an architectural pattern that separates software application logic from the user interface. Originally developed by Microsoft architects Ken Cooper and John Gossman in 2005 as a specialization of the Presentation Model pattern, MVVM became widely adopted through its heavy use in Windows Presentation Foundation (WPF), Silverlight, and later Xamarin.Forms applications. The pattern facilitates the separation of development of the graphical user interface from business logic or back-end logic, making it easier to test, maintain, and evolve applications over time.

The three main components—Model, View, and ViewModel—each have distinct responsibilities. The View handles all UI rendering and user input. The ViewModel acts as an intermediary, exposing data and commands usable by the View while handling presentation logic. The Model represents the underlying data and business logic. This clear separation enables UI developers and back-end developers to work more independently and enables unit testing of business logic without involving the UI.

## Key Concepts

**View** is the visual layer—what the user sees and interacts with. In desktop applications, this might be XAML or HTML/CSS; in mobile, it could be SwiftUI or Jetpack Compose XML. The View has no direct knowledge of the Model or business logic. Instead, it data-binds to the ViewModel, consuming exposed properties and invoking commands.

**ViewModel** serves as the "model of the view"—it holds the state and behavior that the View needs, transformed into a form convenient for display. ViewModels expose properties for data binding (like `IsLoading`, `UserName`, `Items`) and commands (like `SaveCommand`, `DeleteCommand`). A critical feature is that ViewModels know nothing about the View itself, enabling the same ViewModel to power different View implementations.

**Model** encompasses the data and business logic. This includes domain models, repositories, services, and data access code. Models are typically plain objects with no UI-specific dependencies, making them highly testable. They raise property change notifications through interfaces like `INotifyPropertyChanged` in .NET.

**Data Binding** is the mechanism that connects View and ViewModel. Two-way binding allows changes in the View to automatically update the ViewModel and vice versa. One-way binding flows data from source to target. This eliminates much of the "glue code" traditionally needed to synchronize UI and logic.

**Command Pattern** provides a way to encapsulate actions as objects. In MVVM, commands like `RelayCommand` or `DelegateCommand` wrap action handlers, allowing them to be bound to UI elements like buttons without the View needing to know implementation details.

## How It Works

When a user interacts with the View (clicks a button, types in a field), the View sends the command or property change to the bound ViewModel. The ViewModel processes this—often calling Services or Repositories to perform business logic or data operations. If the ViewModel's underlying data changes, it raises a `PropertyChanged` event. The binding system catches this and automatically updates the View.

This unidirectional data flow makes applications more predictable and easier to debug. State changes flow through a clear chain: User Action → View → ViewModel → Model → ViewModel updates → View re-renders.

```csharp
// Example: Simple ViewModel in C# (Xamarin/MAUI style)
public class UserViewModel : INotifyPropertyChanged
{
    private string _name;
    private bool _isLoading;
    private readonly IUserService _userService;

    public UserViewModel(IUserService userService)
    {
        _userService = userService;
        LoadUserCommand = new AsyncRelayCommand(LoadUserAsync);
    }

    public string Name
    {
        get => _name;
        set
        {
            if (_name != value)
            {
                _name = value;
                OnPropertyChanged(nameof(Name));
            }
        }
    }

    public bool IsLoading
    {
        get => _isLoading;
        set => OnPropertyChanged(nameof(IsLoading));
    }

    public IAsyncRelayCommand LoadUserCommand { get; }

    private async Task LoadUserAsync()
    {
        IsLoading = true;
        try
        {
            var user = await _userService.GetCurrentUserAsync();
            Name = user.Name;
        }
        finally
        {
            IsLoading = false;
        }
    }

    public event PropertyChangedEventHandler PropertyChanged;
    protected virtual void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
```

## Practical Applications

MVVM is particularly valuable in scenarios requiring:

- **Complex, data-driven UIs** where forms and data display need to stay synchronized
- **Test-driven development** since business logic in ViewModels can be unit tested independently
- **Team collaboration** allowing designers and developers to work somewhat independently
- **Long-lived applications** that evolve over years, as the separation of concerns reduces coupling

## Related Concepts

- [[model-view-controller]] - Similar pattern with Controller mediating between View and Model
- [[data-binding]] - The mechanism connecting View to ViewModel
- [[software-architecture]] - The broader discipline of structuring software systems
- [[xamarin]] - Mobile framework heavily using MVVM
- [[presentation-model]] - Pattern that influenced MVVM development

## Further Reading

- "Programming WPF" by Chris Sells and Ian Griffiths - Chapter on MVVM
- Microsoft's MVVM Pattern Documentation
- "Essential MVVM" by John P. Smith

## Personal Notes

MVVM can feel like overhead for simple applications, but it pays dividends as complexity grows. The key insight is that ViewModels should be "dummy" about the View—never reference UI types like `Button` or `TextField`. Also, resist the temptation to put too much logic in ViewModels; if your ViewModel becomes a "massive ViewModel," consider whether that logic belongs in a separate Service layer.
