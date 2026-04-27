---
title: "Angular"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [javascript, typescript, frontend, web-development, framework]
---

# Angular

## Overview

Angular is a TypeScript-based web application framework developed by Google. Originally released in 2010 as AngularJS (a JavaScript framework using two-way data binding), it underwent a complete rewrite and was re-released as Angular 2 in 2016. The modern Angular is an entirely different framework that shares only its name with the original. Angular 2+ emphasizes component-based architecture, modularity, and the use of TypeScript for type-safe development.

Angular provides a comprehensive platform for building desktop and mobile web applications. It includes a component model, reactive forms, routing, HTTP client, internationalization support, and a build system powered by the Angular CLI. The framework's opinionated approach offers consistency across large codebases, making it popular for enterprise applications where maintainability and long-term support are priorities.

The framework uses a declarative approach to building UIs, composing applications from components that encapsulate template logic, styles, and behavior. Angular's change detection mechanism tracks modifications to component state and efficiently updates the DOM. The framework supports multiple rendering backends, including the default DOM renderer for browsers and server-side rendering through Angular Universal.

## Key Concepts

**Components**: The fundamental building blocks of Angular applications. A component is a TypeScript class decorated with @Component that contains a template (HTML), styles (CSS), and class logic. Components can contain nested components, forming a tree structure.

**Modules**: Angular applications are organized into NgModules, which group related functionality. Every app has at least one root module (AppModule) and typically includes feature modules that lazy-load specific application sections. Modules provide dependency injection context and organize code into cohesive blocks.

**Services**: Classes annotated with @Injectable that provide application-wide functionality like data fetching, logging, or authentication. Services use Angular's dependency injection system to provide instances to components and other services.

**Templates**: Angular templates extend HTML with syntax for rendering data, handling events, and controlling DOM structure. The template syntax includes interpolation ({{expression}}), property binding ([property]="value"), event binding ((event)="handler"), and two-way binding ([(ngModel)]="value").

**Change Detection**: Angular's mechanism for detecting when component state changes and updating the DOM accordingly. Angular uses Zone.js to automatically detect asynchronous operations that might change state, then runs change detection to reconcile the view with the model.

## How It Works

Angular applications bootstrap from a root module, which bootstraps a root component. The bootstrap process creates the component tree, initializes the application, and attaches the component to a DOM element (typically `<app-root>`). Once running, the application responds to user interactions and data changes through the change detection mechanism.

Component communication happens through several patterns:
- **Input binding**: Parent passes data to child via @Input() properties
- **Output binding**: Child emits events via @Output() EventEmitters
- **Services**: Shared state through injectable services with observables or signals
- **Router**: Navigation state managed by the Angular Router

```typescript
// Example: Simple Angular Component
import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-user-card',
  template: `
    <div class="card">
      <h2>{{ name }}</h2>
      <p>Email: {{ email }}</p>
      <button (click)="onEdit()">Edit</button>
    </div>
  `,
  styles: [`
    .card { border: 1px solid #ccc; padding: 16px; border-radius: 8px; }
    h2 { margin: 0 0 8px; }
  `]
})
export class UserCardComponent {
  @Input() name: string = '';
  @Input() email: string = '';
  @Output() edit = new EventEmitter<void>();

  onEdit(): void {
    this.edit.emit();
  }
}
```

Angular's dependency injection system maintains a hierarchy of injectors. Application-wide services are provided at the root level, while component-specific services can be provided lower in the tree. This allows for different instances or singletons depending on the use case.

## Practical Applications

**Single-Page Applications (SPAs)**: Angular excels at building SPAs where navigation happens without full page reloads. The router manages URL changes and component rendering, providing a smooth user experience.

**Enterprise Dashboards**: Angular's structure and TypeScript's type safety make it suitable for complex data-driven dashboards with multiple visualizations and real-time updates.

**Progressive Web Apps (PWAs)**: Angular includes PWA support through @angular/pwa, enabling offline-capable applications installable on mobile devices.

**E-commerce Platforms**: Large retail sites benefit from Angular's performance optimization features like lazy loading, OnPush change detection, and virtual scrolling for large product lists.

**Content Management Systems**: Angular can power the frontend of headless CMS architectures, consuming APIs and rendering rich content experiences.

## Examples

Building a complete feature with routing and services:

```typescript
// Feature module with routing
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProductListComponent } from './product-list.component';
import { ProductDetailComponent } from './product-detail.component';

const routes: Routes = [
  { path: '', component: ProductListComponent },
  { path: ':id', component: ProductDetailComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProductRoutingModule {}

// Service with HTTP
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Product } from './product.model';

@Injectable({ providedIn: 'root' })
export class ProductService {
  private apiUrl = '/api/products';

  constructor(private http: HttpClient) {}

  getProducts(): Observable<Product[]> {
    return this.http.get<Product[]>(this.apiUrl);
  }

  getProduct(id: string): Observable<Product> {
    return this.http.get<Product>(`${this.apiUrl}/${id}`);
  }
}
```

## Related Concepts

- [[TypeScript]] - The language Angular is built with
- [[React]] - A competing frontend framework
- [[Vue.js]] - Another competing frontend framework
- [[Web Components]] - The browser standard Angular components relate to
- [[Single Page Applications]] - The application pattern Angular uses
- [[Dependency Injection]] - A pattern Angular uses extensively

## Further Reading

- Angular Documentation - Official guides and tutorials at angular.io
- Angular University Blog - In-depth articles on Angular patterns
- "Angular Development with TypeScript" by Yakov Fain - Comprehensive book
- Nrwl Angular Blog - Advanced patterns from the Angular consulting experts

## Personal Notes

Angular's steep learning curve compared to simpler frameworks like React or Vue is a legitimate concern for small projects. However, for large teams building long-lived applications, Angular's opinionated structure pays dividends. Having a standard way to organize modules, services, and components means any Angular developer can quickly understand a new codebase's structure.

The transition to standalone components in Angular 14+ simplified the framework significantly by removing the requirement for NgModules for most use cases. If learning Angular today, start with the standalone component pattern and only introduce NgModules when you need the organizational benefits they provide for very large applications.
