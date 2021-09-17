import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WithNoteComponent } from './with-note.component';

describe('WithNoteComponent', () => {
  let component: WithNoteComponent;
  let fixture: ComponentFixture<WithNoteComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ WithNoteComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(WithNoteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
