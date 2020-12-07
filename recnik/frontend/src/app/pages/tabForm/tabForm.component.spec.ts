import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TabFormComponent } from './tabForm.component';

describe('TabFormComponent', () => {
  let component: TabFormComponent;
  let fixture: ComponentFixture<TabFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [TabFormComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TabFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
