import { Injectable } from '@angular/core';
import { CanDeactivate } from '@angular/router';
import { TabFormComponent } from '../../pages/tabForm/tabForm.component';

@Injectable({
  providedIn: 'root'
})
export class LeaveGuard implements CanDeactivate<TabFormComponent> {

  constructor() { }

  canDeactivate(component: TabFormComponent): boolean {
    if (component.askToLeave) {
      return confirm('Да ли сте сигурни да желите да напустите страницу и изгубите измене?');
    }
    return true;
  }
}
