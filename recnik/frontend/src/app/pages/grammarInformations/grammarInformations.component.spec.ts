import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GrammarInformationsComponent } from './grammarInformations.component';

describe('TabFormComponent', () => {
  let component: GrammarInformationsComponent;
  let fixture: ComponentFixture<GrammarInformationsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [GrammarInformationsComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GrammarInformationsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
